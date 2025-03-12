import hashlib
import hmac
import logging
import os
from datetime import datetime, timedelta
from enum import Enum, IntEnum, auto
from typing import Optional, List, Iterator, Tuple, Iterable

import gmcapsule
from OpenSSL.crypto import X509, load_certificate, FILETYPE_ASN1
from peewee import (
    CharField, BooleanField, ForeignKeyField, Model, IntegerField,
    BlobField, TextField, SqliteDatabase, CompositeKey,
    DateTimeField, fn, SQL, SmallIntegerField
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


class SortType(IntEnum):
    DIFFICULT = 1
    DURATION = 2
    GENRE = 3


class SortDirection(IntEnum):
    ASCEND = 1
    DESCEND = 2


# noinspection DuplicatedCode
class Genre(IntEnum):
    # @formatter:off
    # Adventures
    ADVENTURE = auto()                               # бродилка
    ADVENTURE_SHOOTER = auto()                       # бродилка-стрелялка
    ADVENTURE_SHOOTER_SAFE_CRACK_SIM = auto()        # Бродилка-стрелялка; Симулятор взлома сейфа (КР1)
    ADVENTURE_W_ADVENTURES = auto()                  # бродилка с приключениями
    ADVENTURE_W_ARCADE_ELEMENTS = auto()             # бродилка с элементами аркады
    ADVENTURE_W_BLACK_HUMOR_ELEMENTS = auto()        # бродилка с элементами черного юмора
    ADVENTURE_W_FIGHTING_ELEMENTS = auto()           # бродилка с элементами файтинга
    ADVENTURE_W_FIGHTING_N_PUZZLE_ELEMENTS = auto()  # бродилка с элементами файтинга и головоломками
    ADVENTURE_W_MANAGEMENT_ELEMENTS = auto()         # бродилка с элементами менеджмента
    ADVENTURE_W_HORROR_ELEMENTS = auto()             # бродилка с элементами ужасов
    ADVENTURE_W_AWFUL_HORROR_ELEMENTS = auto()       # бродилка с элементами тихих ужасов
    ADVENTURE_W_LOGIC_ELEMENTS = auto()              # бродилка с логическими элементами
    ADVENTURE_W_LOGIC_PUZZLES = auto()               # бродилка с логическими головоломками
    # Logic
    TRIVIA_GAME = auto()                       # викторина
    TEXT_AND_LOGIC_PUZZLE = auto()             # текстово-логическая головоломка
    PUZZLE = auto()                            # Головоломка (КР1)
    LOGIC_PUZZLE = auto()                      # логическая головоломка
    ARCADE_LOGIC_GAME = auto()                 # аркадно-логическая игра
    LOGIC_GAME = auto()                        # логическая игра
    LOGIC_GAME_W_MANAGEMENT_ELEMENTS = auto()  # логическая игра с элементами менеджмента
    LOGIC_EDUCATIONAL_GAME = auto()            # логико-познавательная игра
    LOGIC_MATH_GAME = auto()                   # логико-математическая игра
    LOGIC_EASEL_SIMULATOR = auto()             # логический симулятор мольберта
    MATH_LOGIC_PUZZLE = auto()                 # логико-математическая головоломка
    MATH_PUZZLE = auto()                       # математическая головоломка
    LOGIC_PUZZLES_AND_MATH_PROBLEMS = auto()   # логические головоломки и математические задачи
    LOGIC_TACTICAL_GAME = auto()               # логико-тактическая игра
    # Simulators
    SIMULATOR = auto()                         # Симулятор (FANS)
    PRISON_SIM = auto()                        # симулятор тюрьмы
    SPACE_RANGERS_SIM = auto()                 # симулятор "космических рейнджеров"
    ANIMAL_LIFE_SIM = auto()                   # симулятор жизни животного
    LAB_RAT_SIM = auto()                       # Симулятор «подопытной крысы» (КР1)
    COMPOSITE_SKETCH_SIM = auto()              # симулятор составления фоторобота
    ECONOMY_SIM = auto()                       # экономический симулятор
    ELECTION_CAMPAIGN_SIM = auto()             # симулятор предвыборной кампании
    HAULER_SIM = auto()                        # симулятор дальнобойщика
    TAXI_SIM = auto()                          # симулятор таксиста
    FISHING_SIM = auto()                       # симулятор рыбалки
    ANCIENT_CARS_RACING_SIM = auto()           # Гонки на древних машинах (КР1)
    RACING_SIM = auto()                        # гоночный симулятор
    RACING_SIM_W_MANAGEMENT_ELEMENTS = auto()  # гоночный симулятор с элементами менеджмента
    PENCHEKRACK_BREEDING_SIM = auto()          # Симулятор выведения пенчекряка (КР1)
    WILD_GOBZAUR_TAMING_SIM = auto()           # Симулятор укрощения дикого гобзавра (КР1)
    PASSING_ENTRANCE_EXAMS = auto()            # Сдача вступительных экзаменов (КР1)
    # Strategies
    TACTICAL_FIGHTING = auto()             # тактический файтинг
    TACTICAL_GAME = auto()                 # тактическая игра
    TACTICAL_STRATEGY = auto()             # тактическая стратегия
    ECONOMIC_STRATEGY = auto()             # экономическая стратегия
    STRATEGY_W_FIGHTING_ELEMENTS = auto()  # стратегия с элементами файтинга
    RECRUITMENT_CENTER_MANAGER = auto()    # менеджер военкомата
    MANAGEMENT = auto()                    # Менеджмент (КР1)
    BUILD_MANAGEMENT = auto()              # Менеджмент; Управление стройкой (КР1)
    SPORT_MANAGEMENT = auto()              # Спорт-менеджер (КР1)
    # Others
    GAMBLING = auto()                          # Азартная игра (КР1)
    TRADING = auto()                           # Торговля (КР1)
    WEAPONS_TESTING = auto()                   # Испытание оружия (КР1)
    ESPIONAGE = auto()                         # Шпионаж (КР1)
    ESPIONAGE_GAMBLING = auto()                # Шпионаж; Азартные игры (КР1)
    ESPIONAGE_BUGGING = auto()                 # Шпионаж; Установка жучков (КР1)
    ASSAULT = auto()                           # Штурм (КР1)
    FANTASY_ROLE_PLAYING_GAME = auto()         # фэнтезийная ролевая игра
    DETECTIVE = auto()                         # детектив
    HUMOROUS_DETECTIVE = auto()                # юмористический детектив
    CARGO_DELIVERY_W_QUEST_ELEMENTS = auto()   # доставка груза с элементами квеста
    FORTRESS_DEFEND = auto()                   # Защита крепости (КР1)
    ACTION_HORROR = auto()                     # Экшн с хоррором (FANS)
    # @formatter:on


class Duration(IntEnum):
    # @formatter:off
    LOW = 1            # низкая
    BELOW_AVERAGE = 2  # ниже средней
    AVERAGE = 3        # средняя
    ABOVE_AVERAGE = 4  # выше средней
    LONG = 5           # высокая
    # @formatter:on


class BaseModel(Model):
    class Meta:
        database = db


class Quest(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=128, null=False)
    file = CharField(max_length=128, null=False)
    lang = CharField(max_length=5, null=False)
    gameVer = CharField(max_length=128, null=False)
    genre = SmallIntegerField(null=True)
    difficult = SmallIntegerField(null=True)
    duration = SmallIntegerField(null=True)

    @staticmethod
    def by(*, qid=None, file=None) -> 'Quest':
        query = Quest.select()
        if qid:
            query = query.where(Quest.id == qid)
        if file:
            query = query.where(Quest.file == file)
        return query.first()

    @staticmethod
    def all_by(*, lang=None, game=None,
               sort_type: SortType = None,
               sort_dir: SortDirection = None) -> Iterator['Quest']:
        query = Quest.select()
        if lang:
            query = query.where(Quest.lang == lang)
        if game and isinstance(game, str):
            query = query.where(Quest.gameVer == game)
        if game and isinstance(game, list):
            query = query.where(Quest.gameVer << game)
        query = query.order_by(Quest.name)
        if sort_dir == SortDirection.ASCEND:
            if sort_type == SortType.DIFFICULT:
                query = query.order_by(Quest.difficult, Quest.duration,
                                       Quest.genre, Quest.name)
            elif sort_type == SortType.DURATION:
                query = query.order_by(Quest.duration, Quest.genre,
                                       Quest.difficult, Quest.name)
            elif sort_type == SortType.GENRE:
                query = query.order_by(Quest.genre, Quest.difficult,
                                       Quest.duration, Quest.name)
        elif sort_dir == SortDirection.DESCEND:
            if sort_type == SortType.DIFFICULT:
                query = query.order_by(-Quest.difficult, -Quest.duration,
                                       -Quest.genre, Quest.name)
            elif sort_type == SortType.DURATION:
                query = query.order_by(-Quest.duration, -Quest.genre,
                                       -Quest.difficult, Quest.name)
            elif sort_type == SortType.GENRE:
                query = query.order_by(-Quest.genre, -Quest.difficult,
                                       -Quest.duration, Quest.name)
        return query.execute()

    @staticmethod
    def count_by(*, lang=None) -> Iterator['Quest']:
        query = Quest.select()
        if lang:
            query = query.where(Quest.lang == lang)
        return query.count()


class Ranger(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=128, null=True, unique=True)
    is_anon = BooleanField(null=False, default=True)
    created = DateTimeField(null=False, default=datetime.now)
    activity = DateTimeField(null=False, default=datetime.now)
    credits_ru = IntegerField(default=2000)
    credits_en = IntegerField(default=2000)
    credits_de = IntegerField(default=2000)
    credits_es = IntegerField(default=2000)

    def get_credits(self, lang):
        if lang == 'ru':
            return self.credits_ru
        elif lang == 'de':
            return self.credits_de
        elif lang == 'es':
            return self.credits_es
        else:
            return self.credits_en

    def set_credits(self, lang, credits):
        if lang == 'ru':
            self.credits_ru = credits
        elif lang == 'de':
            self.credits_de = credits
        elif lang == 'es':
            self.credits_es = credits
        else:
            self.credits_en = credits

    def inc_credits(self, lang, credits):
        if lang == 'ru':
            self.credits_ru += credits
        elif lang == 'de':
            self.credits_de += credits
        elif lang == 'es':
            self.credits_es += credits
        else:
            self.credits_en += credits

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

    @staticmethod
    def leaders(lang) -> Iterable[Tuple[int, str, int, int]]:
        credits_col = Ranger.credits_ru if lang == 'ru' \
            else Ranger.credits_es if lang == 'es' \
            else Ranger.credits_de if lang == 'de' \
            else Ranger.credits_en
        query = (
            Ranger.select(Ranger.id, Ranger.name,
                          fn.count(QuestCompleted.quest).alias('qcc'),
                          credits_col)
            .left_outer_join(Quest, on=(Quest.lang == lang))
            .left_outer_join(QuestCompleted, on=(
                    (QuestCompleted.ranger == Ranger.id)
                    & (QuestCompleted.quest == Quest.id)))
            .where(Ranger.is_anon == False)  # noqa
            .group_by(Ranger.name)
            .order_by(SQL('qcc').desc(), -credits_col, +Ranger.name)
            .limit(10)
        )
        return query.tuples()


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

    sort_type = SmallIntegerField(null=False, default=SortType.DIFFICULT)
    sort_dir = SmallIntegerField(null=False, default=SortDirection.ASCEND)

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

    @staticmethod
    def save_toggle_sort_type(ranger):
        opts = ranger.get_opts()
        sort_type = (opts.sort_type or 1) + 1
        if sort_type > len(SortType):
            sort_type = 1
        (Options.update(sort_type=sort_type)
         .where(Options.ranger == ranger)
         .execute())

    @staticmethod
    def save_toggle_sort_dir(ranger):
        opts = ranger.get_opts()
        sort_dir = (opts.sort_dir or 1) + 1
        if sort_dir > len(SortDirection):
            sort_dir = 1
        (Options.update(sort_dir=sort_dir)
         .where(Options.ranger == ranger)
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
    def by(*, rid, qid=None, lang=None) -> List[int]:
        query = (QuestCompleted.select(QuestCompleted.quest.id)
                 .join(Quest)
                 .where(QuestCompleted.ranger == rid))
        if lang:
            query = query.where(Quest.lang == lang)
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
