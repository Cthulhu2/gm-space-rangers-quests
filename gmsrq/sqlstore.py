import hashlib
import hmac
import logging
import os
import shutil
from datetime import datetime, timedelta
from os.path import islink
from pathlib import Path
from typing import Optional, List

import gmcapsule
from OpenSSL.crypto import X509, load_certificate, FILETYPE_ASN1
from peewee import (
    CharField, BooleanField, ForeignKeyField, Model, IntegerField,
    BlobField, TextField, SqliteDatabase, CompositeKey,
    DateTimeField
)

from gmsrq.store import load_lang, load_ansi, load_state
from srqmplayer.qmplayer.funcs import GameState, PlayerState, GameStateEnum

db = SqliteDatabase(
    'gmsrq.sqlite',
    # https://www.sqlite.org/pragma.html
    pragmas={'journal_mode': 'wal',
             'foreign_keys': 1,
             'synchronous': 1})

log = logging.getLogger()
PASS_EXPIRE = timedelta(minutes=30)


class BaseModel(Model):
    class Meta:
        database = db


class Quest(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=128, null=False)
    file = CharField(max_length=128, null=False)
    lang = CharField(max_length=5, null=False)
    gameVer = CharField(max_length=128, null=False)

    @staticmethod
    def by(*, qid=None, file=None) -> 'Quest':
        if qid and file:
            return Quest.select().where((Quest.id == qid)
                                        & (Quest.file == file)).first()
        elif qid:
            return Quest.select().where(Quest.id == qid).first()
        elif file:
            return Quest.select().where(Quest.file == file).first()
        else:
            raise Exception('Quest id or file required')


class Ranger(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=128, null=True, unique=True)
    is_anon = BooleanField(null=False, default=True)
    created = DateTimeField(null=False, default=datetime.now)
    activity = DateTimeField(null=False, default=datetime.now)

    def get_opts(self) -> 'Options':
        return self._opts.first()

    def get_certs(self) -> List['Cert']:
        return list(self._certs)

    @staticmethod
    def exists_name(name):
        return Ranger.select().where(Ranger.name == name).exists()

    @staticmethod
    def by(*, fp_cert=None, name=None) -> 'Ranger':
        if fp_cert and name:
            return (Ranger.select().join(Cert)
                    .where((Cert.fp == fp_cert)
                           & (Ranger.name == name))
                    .first())
        elif fp_cert:
            return Ranger.select().join(Cert).where(Cert.fp == fp_cert).first()
        elif name:
            return Ranger.select().where(Ranger.name == name).first()
        else:
            raise Exception('fp_cert or name required')

    @staticmethod
    def create_anon(ident: gmcapsule.Identity):
        cert = Cert.by(fp_cert=ident.fp_cert)
        if cert and cert.subj is not None:
            return  #
        cn = ident.subject()['CN'] if 'CN' in ident.subject() else 'None'
        x509: X509 = load_certificate(FILETYPE_ASN1, ident.cert)
        not_after = x509.get_notAfter().decode('ascii')
        not_after = datetime.strptime(not_after, '%Y%m%d%H%M%SZ')
        if not cert:
            anon = Ranger.create()
            Options.create(ranger=anon, passWhen=None)
            Cert.create(ranger=anon, fp=ident.fp_cert,
                        subj=cn, expire=not_after)
        elif cert.subj is None:
            cert.subj = cn
            cert.expire = not_after
            cert.save()

    @staticmethod
    def create_anon_fp(fp_cert):
        cert = Cert.by(fp_cert=fp_cert)
        if cert:
            return  #
        anon = Ranger.create()
        Options.create(ranger=anon, passWhen=None)
        Cert.create(ranger=anon, fp=fp_cert, subj=None, expire=None)

    @staticmethod
    def import_registered(name, certs_info: List[Path]):
        ranger = Ranger.by(name=name)
        if ranger:
            return  #
        ranger = Ranger.create(name=name, is_anon=False)
        Options.create(ranger=ranger, passWhen=None)
        for ci in certs_info:
            with open(ci, 'r') as f:
                cn = f.readline().strip()
                not_after = f.readline().strip()
                not_after = datetime.strptime(not_after, '%Y%m%d%H%M%SZ')
            Cert.create(ranger=ranger, fp=ci.name[0:-5],  # strip '.info'
                        subj=cn, expire=not_after)


class Cert(BaseModel):
    ranger = ForeignKeyField(Ranger, backref='_certs', column_name='rId')
    fp = CharField(max_length=64, primary_key=True)
    subj = CharField(max_length=256, null=True)
    expire = DateTimeField(null=True)

    class Meta:
        indexes = ((('ranger',), False),
                   (('fp',), False))

    @staticmethod
    def by(*, fp_cert=None) -> Optional['Cert']:
        return (Cert.select()
                .where(Cert.fp == fp_cert)
                .first())


class Options(BaseModel):
    ranger = ForeignKeyField(Ranger, column_name='rId', backref='_opts',
                             primary_key=True, on_delete='cascade')

    ansi = BooleanField(null=False, default=False)
    lang = CharField(max_length=5, null=False, default='en')

    passHash = BlobField(null=True)
    passSalt = BlobField(null=True)
    passWhen = DateTimeField(null=True, default=None)

    class Meta:
        indexes = ((('ranger',), False),)

    @staticmethod
    def lang_by(*, fp_cert=None):
        ranger = Ranger.select().join(Cert).where(Cert.fp == fp_cert).first()
        return ranger.get_opts().lang if ranger else 'en'

    @staticmethod
    def save_lang(fp_cert, lang):
        ranger = Ranger.select().join(Cert).where(Cert.fp == fp_cert)
        Options.update(lang=lang).where(Options.ranger << ranger).execute()

    def get_pass_expires(self) -> Optional[datetime]:
        return self.passWhen + timedelta(minutes=30) if self.passWhen else None

    @staticmethod
    def is_valid_pass(username, password) -> bool:
        ranger: Ranger = Ranger.select().where(Ranger.name == username).first()
        opts = ranger.get_opts() if ranger else None

        if (opts and opts.passHash and opts.passWhen and opts.passSalt
                and (opts.passWhen + PASS_EXPIRE) > datetime.utcnow()):
            sha256 = hashlib.pbkdf2_hmac('sha256', password.encode(),
                                         opts.passSalt, 100)
            return hmac.compare_digest(opts.passHash, sha256)
        return False

    @staticmethod
    def save_pass(fp_cert, password: str):
        ranger = Ranger.select().join(Cert).where(Cert.fp == fp_cert)
        if password:
            salt = os.urandom(16)
            sha256 = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100)
            (Options.update(passHash=sha256, passSalt=salt,
                            passWhen=datetime.utcnow())
             .where(Options.ranger << ranger)
             .execute())
        else:
            (Options.update(passHash=None, passSalt=None, passWhen=None)
             .where(Options.ranger << ranger)
             .execute())


class QuestState(BaseModel):
    ranger = ForeignKeyField(Ranger, column_name='rId', on_delete='cascade')
    quest = ForeignKeyField(Quest, column_name='qId')
    state = TextField(null=False)
    sId = IntegerField(null=False)

    class Meta:
        primary_key = CompositeKey('ranger', 'quest')

    @staticmethod
    def by(*, fp_cert, qid) -> Optional['QuestState']:
        return (QuestState.select()
                .join(Quest)
                .switch(QuestState)
                .join(Ranger)
                .join(Cert)
                .where((Cert.fp == fp_cert) & (Quest.id == qid))
                .first())

    @staticmethod
    def save_state(fp_cert, qid, sid, state: GameState):
        if q_state := QuestState.by(fp_cert=fp_cert, qid=qid):
            q_state.state = state.to_json()
            q_state.sId = sid
            q_state.save()
        else:
            ranger = Ranger.by(fp_cert=fp_cert)
            QuestState.create(ranger=ranger, quest=qid, sId=sid,
                              state=state.to_json())
        return sid, state

    @staticmethod
    def save_state_by_name(name, qid, sid, state: GameState):
        q_state = (QuestState.select()
                   .join(Quest)
                   .switch(QuestState)
                   .join(Ranger)
                   .where((Ranger.name == name) & (Quest.id == qid))
                   .first())
        if q_state:
            q_state.state = state.to_json()
            q_state.sId = sid
            q_state.save()
        else:
            ranger = Ranger.by(name=name)
            QuestState.create(ranger=ranger, quest=qid, sId=sid,
                              state=state.to_json())
        return sid, state

    @staticmethod
    def del_state_at_the_end(state: PlayerState, fp_cert, qid):
        if state.gameState == GameStateEnum.running:
            return  # do nothing
        if q_state := QuestState.by(fp_cert=fp_cert, qid=qid):
            q_state.delete_instance()


class IpOptions(BaseModel):
    addr = TextField(primary_key=True)
    lang = CharField(max_length=5, null=False, default='en')

    @staticmethod
    def by(*, addr):
        return IpOptions.select().where(IpOptions.addr == addr).first()

    @staticmethod
    def lang_by_ip(addr):
        opts = IpOptions.by(addr=addr)
        return opts.lang if opts else 'en'

    @staticmethod
    def save_lang(addr, lang):
        if opts := IpOptions.by(addr=addr):
            opts.lang = lang
            opts.save()
        else:
            IpOptions.create(addr=addr, lang=lang)


def import_users(users_dir):
    registered_ranger_certs_links: List[Path] = []
    ip_addr_dirs: List[Path] = []
    empty_dirs: List[Path] = []
    registered_ranger_dirs: List[Path] = []
    anon_cert_dir: List[Path] = []

    for it in Path(users_dir).iterdir():
        if islink(it):
            registered_ranger_certs_links.append(it)
        elif it.is_file():
            pass
        elif len(it.name.split('.')) == 4:
            ip_addr_dirs.append(it)
        elif is_empty_dir(it):
            empty_dirs.append(it)
        elif next(it.glob('*.info'), None):
            registered_ranger_dirs.append(it)
        else:
            anon_cert_dir.append(it)

    for it in empty_dirs:
        log.info(f'Remove empty dir {it.name}')
        shutil.rmtree(it)

    for it in registered_ranger_certs_links:
        log.info(f'Remove cert links {it.name}')
        it.unlink(missing_ok=True)

    for it in ip_addr_dirs:
        log.info(f'Import IP sessions {it.name}')
        lang = load_lang(users_dir, it.name)
        IpOptions.save_lang(it.name, lang=lang)
        shutil.rmtree(it)

    with db.atomic():
        for it in anon_cert_dir:
            log.info(f'Import anon ranger {it.name}')
            Ranger.create_anon_fp(it.name)
            ranger = Ranger.by(fp_cert=it.name)
            ranger.created = datetime.fromtimestamp(os.path.getmtime(it))
            ranger.activity = datetime.fromtimestamp(os.path.getmtime(it))
            ranger.save()
            opts = ranger.get_opts()
            opts.lang = load_lang(users_dir, it.name)
            opts.ansi = load_ansi(users_dir, it.name)
            opts.save()
            for quest_dir in it.iterdir():
                if not quest_dir.is_dir() or is_empty_dir(quest_dir):
                    continue
                log.info(f'Import anon ranger {it.name} quest {quest_dir.name}')
                sid, state = load_state(users_dir, it.name, quest_dir.name)
                if state:
                    quest = Quest.by(file=quest_dir.name)
                    QuestState.save_state(it.name, quest.id, sid, state)
    for it in anon_cert_dir:
        log.info(f'Remove anon dir {it.name}')
        shutil.rmtree(it)

    with db.atomic():
        for it in registered_ranger_dirs:
            log.info(f'Import registered ranger {it.name}')
            certs = [*it.glob('*.info')]
            Ranger.import_registered(it.name, certs)
            #
            ranger = Ranger.by(name=it.name)
            ranger.created = datetime.fromtimestamp(os.path.getmtime(it))
            ranger.activity = datetime.fromtimestamp(os.path.getmtime(it))
            ranger.save()
            opts = ranger.get_opts()
            opts.lang = load_lang(users_dir, it.name)
            opts.ansi = load_ansi(users_dir, it.name)
            opts.save()
            for quest_dir in it.iterdir():
                if not quest_dir.is_dir() or is_empty_dir(quest_dir):
                    continue
                log.info(f'Import registered ranger {it.name}'
                         f' quest {quest_dir.name}')
                sid, state = load_state(users_dir, it.name, quest_dir.name)
                if state:
                    quest = Quest.by(file=quest_dir.name)
                    QuestState.save_state_by_name(it.name, quest.id, sid, state)

    for it in registered_ranger_dirs:
        log.info(f'Remove registered ranger dir {it.name}')
        shutil.rmtree(it)


def is_empty_dir(dir_: Path):
    sub = os.listdir(dir_)
    if not sub:
        return True
    return all(list(map(
        lambda it: (Path(dir_).joinpath(it).is_dir()
                    and is_empty_dir(Path(dir_).joinpath(it))),
        sub)))
