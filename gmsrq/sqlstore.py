import hashlib
import hmac
import logging
import os
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List, Iterator

import gmcapsule
from OpenSSL.crypto import X509, load_certificate, FILETYPE_ASN1
from peewee import (
    CharField, BooleanField, ForeignKeyField, Model, IntegerField,
    BlobField, TextField, SqliteDatabase, CompositeKey,
    DateTimeField, fn
)

from srqmplayer.qmplayer import Player
from srqmplayer.qmplayer.funcs import GameState, PlayerState, GameStateEnum

db = SqliteDatabase(
    'gmsrq.sqlite',
    # https://www.sqlite.org/pragma.html
    pragmas={'journal_mode': 'wal',
             'foreign_keys': 1,
             'synchronous': 1,
             'journal_size_limit': 1024 * 512})

log = logging.getLogger()
PASS_EXPIRE = timedelta(minutes=30)

# 1 Venus, 2 Earth, 3 Mars
SOL_INHABITED = [1, 2, 3]
# 0 Mercury, 4 Jupiter, 5 Saturn, 6 Neptune, 7 Uranus, 8 Pluto
SOL_UNINHABITED = [0, 4, 5, 6, 7, 8]


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
        query = Quest.select()
        if qid:
            query = query.where(Quest.id == qid)
        if file:
            query = query.where(Quest.file == file)
        return query.first()

    @staticmethod
    def all_by(*, lang=None, game=None) -> Iterator['Quest']:
        query = Quest.select()
        if lang:
            query = query.where(Quest.lang == lang)
        if game and isinstance(game, str):
            query = query.where(Quest.gameVer == game)
        if game and isinstance(game, list):
            query = query.where(Quest.gameVer << game)
        return query.order_by(Quest.name).execute()


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
        return Ranger.select().where(Ranger.name ** name).exists()

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
    def update_activity(fp_cert):
        (Ranger.update(activity=datetime.now()).from_(Cert)
         .where((Cert.fp == fp_cert) & (Ranger.id == Cert.ranger))
         .execute())


class Cert(BaseModel):
    ranger = ForeignKeyField(Ranger, backref='_certs', column_name='rId',
                             on_delete='cascade')
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
        ranger = Ranger.by(fp_cert=fp_cert)
        return ranger.get_opts().lang if ranger else 'en'

    @staticmethod
    def save_lang(fp_cert, lang):
        ranger = Ranger.select().join(Cert).where(Cert.fp == fp_cert)
        Options.update(lang=lang).where(Options.ranger << ranger).execute()

    def get_pass_expires(self) -> Optional[datetime]:
        expires = self.passWhen + PASS_EXPIRE if self.passWhen else None
        if expires and expires < datetime.utcnow():
            (Options.update(passHash=None, passSalt=None, passWhen=None)
             .where(Options.ranger == self.ranger)
             .execute())
        return expires

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
    fromStar = TextField(null=True)
    fromPlanet = TextField(null=True)
    toStar = TextField(null=True)
    toPlanet = TextField(null=True)

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
    def in_progress(*, rid) -> List[int]:
        return list(QuestState.select(QuestState.quest.id)
                    .join(Quest)
                    .where((QuestState.ranger == rid) & (QuestState.sId != 0))
                    .scalars())

    @staticmethod
    def save_state(fp_cert, qid, sid, state: GameState, p: Player):
        if q_state := QuestState.by(fp_cert=fp_cert, qid=qid):
            q_state.state = state.to_json()
            q_state.sId = sid
            q_state.save()
        else:
            ranger = Ranger.by(fp_cert=fp_cert)
            QuestState.create(ranger=ranger, quest=qid, sId=sid,
                              state=state.to_json(),
                              fromStar=p.FromStar, fromPlanet=p.FromPlanet,
                              toStar=p.ToStar, toPlanet=p.ToPlanet)
        return sid, state

    @staticmethod
    def del_state_at_the_end(state: PlayerState, fp_cert, qid, rid):
        if state.gameState == GameStateEnum.running:
            return  # do nothing
        if q_state := QuestState.by(fp_cert=fp_cert, qid=qid):
            q_state.delete_instance()
        if state.gameState == GameStateEnum.win:
            QuestCompleted.get_or_create(ranger=rid, quest=qid)


class QuestCompleted(BaseModel):
    ranger = ForeignKeyField(Ranger, column_name='rId', backref='_completed',
                             on_delete='cascade')
    quest = ForeignKeyField(Quest, column_name='qId')

    class Meta:
        primary_key = CompositeKey('ranger', 'quest')
        indexes = ((('ranger',), False),
                   (('quest',), False),)

    @staticmethod
    def save_by(*, rid, qid):
        completed = (QuestCompleted.select()
                     .where((QuestCompleted.ranger == rid)
                            & (QuestCompleted.quest == qid))
                     .first())
        if not completed:
            QuestCompleted.create(ranger=rid, quest=qid)

    @staticmethod
    def by(*, rid, qid=None) -> List[int]:
        query = (QuestCompleted.select(QuestCompleted.quest.id)
                 .join(Quest)
                 .where(QuestCompleted.ranger == rid))
        if qid:
            return list(query.where(QuestCompleted.quest == qid).scalars())
        return list(query.scalars())


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


class Star(BaseModel):
    id = IntegerField(null=False)
    lang = CharField(max_length=5, null=False)
    name = CharField(max_length=50, null=False)
    size = CharField(max_length=50, null=True)

    class Meta:
        primary_key = CompositeKey('id', 'lang')
        indexes = ((('id', 'lang'), False),
                   (('lang',), False),
                   (('name',), False),)

    @staticmethod
    def choice_by(*, lang, include_sol: bool = True, but: int = None) -> 'Star':
        query = Star.select().where(Star.lang == lang)
        if not include_sol:
            query = query.where(Star.id != 2)
        if but is not None:
            query = query.where(Star.id != but)
        return query.order_by(fn.Random()).first()


class PlanetRace(Enum):
    Maloc = 'Maloc'
    Peleng = 'Peleng'
    People = 'People'
    Fei = 'Fei'
    Gaal = 'Gaal'
    No = 'No'
    PirateClan = 'PirateClan'
    Solar = 'Solar'


class Planet(BaseModel):
    id = IntegerField(null=False)
    lang = CharField(max_length=5, null=False)
    race = CharField(max_length=10, null=False)
    name = CharField(max_length=50, null=False)

    class Meta:
        primary_key = CompositeKey('id', 'lang', 'race')
        indexes = ((('id', 'lang', 'race'), False),
                   (('lang', 'race'), False),
                   (('name',), False),)

    @staticmethod
    def choice_by(*, lang,
                  race: List[str] = None,
                  in_sol: bool = False,
                  but: int = None) -> 'Planet':
        query = Planet.select().where(Planet.lang == lang)
        if in_sol:
            query = query.where(Planet.race == PlanetRace.Solar.value)
            if PlanetRace.No.value in race:
                query = query.where(Planet.id << SOL_UNINHABITED)
            else:
                query = query.where(Planet.id << SOL_INHABITED)
        elif race:
            query = query.where(Planet.race << race)
        if but is not None:
            query = query.where(Planet.id != but)
        return query.order_by(fn.Random()).first()
