# Copyright © 2017 Tom Hacohen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, version 3.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import vobject
import json
import os
import peewee

from .crypto import CryptoManager, AsymmetricCryptoManager, AsymmetricKeyPair, derive_key, CURRENT_VERSION
from .service import JournalManager, EntryManager, SyncEntry
from . import cache, pim, service, db, exceptions

API_URL = 'https://api.etesync.com/'

# Expose the authenticator
Authenticator = service.Authenticator


class EteSync:
    def __init__(self, email, auth_token, remote=API_URL, cipher_key=None, db_path=None):
        self.email = email
        self.auth_token = auth_token
        self.remote = remote
        self.cipher_key = cipher_key

        self._init_db(db_path)

    def reinit(self):
        self._set_db(self._database)

    def _set_db(self, database):
        self._database = database

        db.database_proxy.initialize(database)

        self._init_db_tables(database)

        self.user, created = cache.User.get_or_create(username=self.email)

    def _init_db(self, db_path):
        from playhouse.sqlite_ext import SqliteExtDatabase

        if db_path is None:
            db_path = os.path.join(os.path.expanduser('~'), '.etesync', 'data.db')

        directory = os.path.dirname(db_path)
        if directory != '' and not os.path.exists(directory):
            os.makedirs(directory)

        database = SqliteExtDatabase(db_path, pragmas={
            'journal_mode': 'wal',
            'foreign_keys': 1,
            })
        database.connect()

        self._set_db(database)

    def _init_db_tables(self, database, additional_tables=None):
        CURRENT_DB_VERSION = 2

        new_db = not database.table_exists('journalentity')

        database.create_tables([cache.Config, pim.Content, cache.User, cache.JournalEntity,
                                cache.EntryEntity, cache.UserInfo], safe=True)
        if additional_tables:
            database.create_tables(additional_tables, safe=True)

        default_db_version = CURRENT_DB_VERSION if new_db else 0
        config, created = cache.Config.get_or_create(defaults={'db_version': default_db_version})

        if config.db_version < 1:
            from playhouse.migrate import SqliteMigrator, migrate
            # Essentially version 0 so do first migration.
            migrator = SqliteMigrator(database)

            try:
                migrate(
                    migrator.add_column('journalentity', 'read_only', cache.JournalEntity.read_only),
                )
            except peewee.OperationalError:
                # A hack because we don't have a db config yet.
                pass

            config.db_version = 1
            config.save()


        if config.db_version < 2:
            from playhouse.migrate import SqliteMigrator, migrate
            migrator = SqliteMigrator(database)

            migrate(
                migrator.add_column('journalentity', 'remote_last_uid', cache.JournalEntity.remote_last_uid),
            )

            config.db_version = 2
            config.save()

    def get_or_create_user_info(self, force_fetch=False):
        user_info = None
        try:
            user_info = cache.UserInfo.get(user=self.user)
        except cache.UserInfo.DoesNotExist:
            pass

        if user_info is None or force_fetch:
            info_manager = service.UserInfoManager(self.remote, self.auth_token)
            remote_info = None
            try:
                remote_info = info_manager.get(self.user.username, self.cipher_key)
            except exceptions.HttpNotFound:
                pass

            if remote_info:
                remote_info.verify()
            else:
                key_pair = AsymmetricCryptoManager.generate_key_pair()
                crypto_manager = CryptoManager(CURRENT_VERSION, self.cipher_key, b'userInfo')
                remote_info = service.RawUserInfo(crypto_manager, self.user.username, key_pair.public_key)
                remote_info.update(key_pair.private_key)
                remote_info.verify()
                info_manager.add(remote_info)

            new_user_info = user_info is None
            user_info = cache.UserInfo(user=self.user, pubkey=remote_info.pubkey, content=remote_info.getContent())
            user_info.save(force_insert=new_user_info)

        return user_info

    def sync(self):
        self.get_or_create_user_info(force_fetch=True)
        self.sync_journal_list()
        for journal in self.list():
            self.sync_journal(journal.uid)

    def sync_journal_list(self):
        self.push_journal_list()
        manager = JournalManager(self.remote, self.auth_token)

        existing = {}
        for journal in self.list():
            existing[journal.uid] = journal._cache_obj

        for entry in manager.list(self.cipher_key):
            entry.crypto_manager = self._get_journal_cryptomanager(entry)
            entry.verify()
            if entry.uid in existing:
                journal = existing[entry.uid]
                del existing[journal.uid]
            else:
                journal = cache.JournalEntity(local_user=self.user, uid=entry.uid, owner=entry.owner)

            journal.version = entry.version
            journal.encrypted_key = entry.encrypted_key
            journal.read_only = entry.read_only
            journal.remote_last_uid = entry.remote_last_uid
            journal.content = entry.getContent()
            journal.save()

        # Delete remaining
        for journal in existing.values():
            journal.deleted = True
            journal.save()

    def _journal_list_dirty_get(self):
        return self.user.journals.where(cache.JournalEntity.dirty | cache.JournalEntity.new)

    def journal_list_is_dirty(self):
        changed = list(self._journal_list_dirty_get())
        return len(changed) > 0

    def push_journal_list(self):
        manager = JournalManager(self.remote, self.auth_token)

        changed = self._journal_list_dirty_get()

        for journal in changed:
            crypto_manager = self._get_journal_cryptomanager(journal)
            raw_journal = service.RawJournal(crypto_manager, uid=journal.uid)
            raw_journal.update(journal.content)

            if journal.deleted:
                manager.delete(raw_journal)
            elif journal.new:
                manager.add(raw_journal)
                journal.new = False
            else:
                manager.update(raw_journal)

            journal.dirty = False
            journal.save()

    def sync_journal(self, uid):
        # FIXME: At the moment if there's a conflict remote would win.
        self.pull_journal(uid)
        self.push_journal(uid)

    def _get_journal_cryptomanager(self, journal):
        if journal.encrypted_key is not None:
            # If journal is pubkey encrypted, fetch encryption key
            user_info = self.get_or_create_user_info()
            key_pair = AsymmetricKeyPair(user_info.content, user_info.pubkey)
            return CryptoManager.create_from_asymmetric_encryted_key(
                    journal.version, key_pair, journal.encrypted_key)
        else:
            cipher_key = self.cipher_key
            return CryptoManager(journal.version, cipher_key, journal.uid.encode())

    def _get_last_entry(self, journal):
        try:
            return journal.entries.order_by(cache.EntryEntity.id.desc()).get()
        except cache.EntryEntity.DoesNotExist:
            return None

    def pull_journal(self, uid):
        journal_uid = uid
        manager = EntryManager(self.remote, self.auth_token, journal_uid)

        journal = cache.JournalEntity.get(local_user=self.user, uid=journal_uid)
        crypto_manager = self._get_journal_cryptomanager(journal)

        collection = Journal._from_cache(journal).collection

        prev = self._get_last_entry(journal)
        last_uid = None if prev is None else prev.uid

        if (last_uid is not None) and (last_uid == journal.remote_last_uid):
            return

        for entry in manager.list(crypto_manager, last_uid):
            entry.verify(prev)
            content = entry.getContent()
            syncEntry = SyncEntry.from_json(content.decode())
            collection.apply_sync_entry(syncEntry)
            cache.EntryEntity.create(uid=entry.uid, content=content, journal=journal)

            prev = entry

    def _journal_dirty_get(self, journal):
        return journal.content_set.where(pim.Content.new | pim.Content.dirty | pim.Content.deleted)

    def journal_is_dirty(self, uid):
        journal = cache.JournalEntity.get(local_user=self.user, uid=uid)
        changed = list(self._journal_dirty_get(journal))
        return len(changed) > 0

    def push_journal(self, uid):
        # FIXME: Implement pushing in chunks
        journal_uid = uid
        manager = EntryManager(self.remote, self.auth_token, journal_uid)

        journal = cache.JournalEntity.get(local_user=self.user, uid=journal_uid)
        crypto_manager = self._get_journal_cryptomanager(journal)
        changed_set = self._journal_dirty_get(journal)
        changed = list(changed_set)

        if len(changed) == 0:
            return

        prev = self._get_last_entry(journal)
        last_uid = None if prev is None else prev.uid

        entries = []
        for pim_entry in changed:
            if pim_entry.deleted:
                action = 'DELETE'
            elif pim_entry.new:
                action = 'ADD'
            else:
                action = 'CHANGE'
            sync_entry = SyncEntry(action, pim_entry.content)
            raw_entry = service.RawEntry(crypto_manager)
            raw_entry.update(sync_entry.to_json().encode(), prev)
            entries.append(raw_entry)

            prev = raw_entry

        manager.add(entries, last_uid)

        # Add entries to cache
        for entry in entries:
            cache.EntryEntity.create(uid=entry.uid, content=entry.getContent(), journal=journal)

        # Clear dirty flags and delete deleted content
        pim.Content.delete().where((pim.Content.journal == journal) & pim.Content.deleted).execute()
        pim.Content.update(new=False, dirty=False).where(
                (pim.Content.journal == journal) & (pim.Content.new | pim.Content.dirty)
            ).execute()

    def derive_key(self, password):
        self.cipher_key = derive_key(password, self.email)
        return self.cipher_key

    # CRUD operations
    def list(self):
        for cache_obj in self.user.journals.where(~cache.JournalEntity.deleted):
            yield Journal._from_cache(cache_obj)

    def get(self, uid):
        try:
            return Journal._from_cache(self.user.journals.where(
                (cache.JournalEntity.uid == uid) & ~cache.JournalEntity.deleted).get())
        except cache.JournalEntity.DoesNotExist as e:
            raise exceptions.DoesNotExist(e)


class ApiObjectBase:
    def __init__(self):
        self._cache_obj = None

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.uid)

    @classmethod
    def _from_cache(cls, cache_obj):
        ret = cls()
        ret._cache_obj = cache_obj
        return ret

    @classmethod
    def create(cls, journal, uid, content):
        cache_obj = cls._CACHE_OBJ_CLASS()
        cache_obj.journal = journal._cache_obj
        cache_obj.uid = uid
        cache_obj.content = content
        cache_obj.new = True
        return cls._from_cache(cache_obj)

    @property
    def uid(self):
        if self._cache_obj.uid is None:
            return None
        return str(self._cache_obj.uid)

    @uid.setter
    def uid(self, uid):
        self._cache_obj.uid = uid

    @property
    def content(self):
        return self._cache_obj.content

    @content.setter
    def content(self, content):
        self._cache_obj.content = content

    def save(self):
        try:
            self._cache_obj.save()
        except peewee.IntegrityError as e:
            if 'UNIQUE' in str(e):
                raise exceptions.AlreadyExists(e)
            else:
                raise exceptions.DoesNotExist(e)


class Entry(ApiObjectBase):
    _CACHE_OBJ_CLASS = cache.EntryEntity


class PimObject(ApiObjectBase):
    _CACHE_OBJ_CLASS = pim.Content

    @classmethod
    def create(cls, collection, content):
        if collection.get_content_class() != cls:
            raise exceptions.TypeMismatch('Collection "{}" does not allow "{}" children.'.format(
                collection.__class__.__name__, cls.__name__))
        ret = super().create(collection.journal, None, None)
        ret.content = content
        if ret.uid is None:
            return None
        return ret

    @property
    def content(self):
        return self._cache_obj.content

    @content.setter
    def content(self, content):
        self._cache_obj.content = content
        self.uid = self.__class__.get_uid(content)

    def delete(self):
        self._cache_obj.deleted = True
        self._cache_obj.save()

    def save(self):
        self._cache_obj.dirty = True
        super().save()


class Event(PimObject):
    @classmethod
    def get_uid(cls, content):
        vobj = vobject.readOne(content)
        try:
            return vobj.vevent.uid.value
        except AttributeError:
            return None


class Contact(PimObject):
    @classmethod
    def get_uid(cls, content):
        vobj = vobject.readOne(content)
        try:
            return vobj.uid.value
        except AttributeError:
            return None


class Task(PimObject):
    @classmethod
    def get_uid(cls, content):
        vobj = vobject.readOne(content)
        try:
            return vobj.vtodo.uid.value
        except AttributeError:
            return None


class BaseCollection:
    def __init__(self, journal):
        self._journal = journal
        self._cache_obj = journal._cache_obj
        if self._journal.info is None:
            self.update_info(None)

    @property
    def display_name(self):
        return self._journal.info.get('displayName')

    @property
    def description(self):
        return self._journal.info.get('description')

    @property
    def journal(self):
        return self._journal

    def update_info(self, update_info):
        if update_info is None:
            self._journal.update_info(self._get_default_info())
        else:
            self._journal.update_info(update_info)

    def _get_default_info(self):
        return {'type': self.__class__.TYPE, 'readOnly': False, 'selected': True}

    def apply_sync_entry(self, sync_entry):
        journal = self._cache_obj
        uid = self.get_content_class().get_uid(sync_entry.content)
        if uid is None:
            print("WARNING: uid not found for entry, skipping. Content:")
            print(sync_entry.content)
            return

        try:
            content = pim.Content.get(uid=uid, journal=journal)
        except pim.Content.DoesNotExist:
            content = None

        if sync_entry.action == 'DELETE':
            if content is not None:
                content.delete_instance()
            else:
                print("WARNING: Failed to delete " + uid)

            return

        content = pim.Content(journal=journal, uid=uid) if content is None else content

        content.content = sync_entry.content
        content.save()

    # CRUD
    def list(self):
        for content in self._cache_obj.content_set.where(~pim.Content.deleted):
            yield self.get_content_class()._from_cache(content)

    def get(self, uid):
        try:
            return self.get_content_class()._from_cache(self._cache_obj.content_set.where(pim.Content.uid == uid).get())
        except pim.Content.DoesNotExist as e:
            raise exceptions.DoesNotExist(e)

    @classmethod
    def create(cls, etesync, uid, content):
        cache_obj = cache.JournalEntity(new=True)
        cache_obj.local_user = etesync.user
        cache_obj.uid = uid
        cache_obj.version = CURRENT_VERSION

        ret = cls(Journal._from_cache(cache_obj))
        ret.update_info(content)
        return ret

    def delete(self):
        self._cache_obj.deleted = True
        self._cache_obj.dirty = True
        self._cache_obj.save()

    def save(self):
        self._cache_obj.dirty = True
        try:
            self._cache_obj.save()
        except peewee.IntegrityError as e:
            raise exceptions.AlreadyExists(e)


class Calendar(BaseCollection):
    TYPE = 'CALENDAR'

    def get_content_class(self):
        return Event


class TaskList(BaseCollection):
    TYPE = 'TASKS'

    def get_content_class(self):
        return Task


class AddressBook(BaseCollection):
    TYPE = 'ADDRESS_BOOK'

    def get_content_class(self):
        return Contact


class Journal(ApiObjectBase):
    @property
    def version(self):
        return self._cache_obj.version

    @property
    def read_only(self):
        return self._cache_obj.read_only

    @property
    def collection(self):
        journal_info = self.info
        if journal_info.get('type') == AddressBook.TYPE:
            return AddressBook(self)
        elif journal_info.get('type') == Calendar.TYPE:
            return Calendar(self)
        elif journal_info.get('type') == TaskList.TYPE:
            return TaskList(self)

    @property
    def info(self):
        if self._cache_obj.content is not None:
            return json.loads(self._cache_obj.content.decode())

    def update_info(self, update_info):
        if update_info is None:
            raise RuntimeError("update_info can't be None.")
        else:
            journal_info = self.info
            if journal_info is None:
                journal_info = {}
            journal_info.update(update_info)
        self._cache_obj.content = json.dumps(journal_info, ensure_ascii=False).encode()

    # CRUD
    def list(self):
        for entry in self._cache_obj.entries:
            yield Entry._from_cache(entry)
