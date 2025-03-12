import gmcapsule
import pytest
from OpenSSL.crypto import load_certificate, FILETYPE_PEM
from peewee_migrate import Router

from gmsrq import MIGRATE_DIR
from gmsrq.sqlstore import Ranger, Cert, IpOptions, Options, Quest, \
    QuestState, QuestCompleted, Planet, Star, SOL_INHABITED, SOL_UNINHABITED
from srqmplayer.alea import AleaState
from srqmplayer.formula import ParamValues
from srqmplayer.qmplayer import DEFAULT_PLAYERS
from srqmplayer.qmplayer.funcs import GameState, State, PlayerState, \
    GameStateEnum
# noinspection PyUnresolvedReferences
from . import temp_db, TEST_RESOURCE_DIR

GAME_STATE = GameState(
    state=State.starting, critParamId=-1, locationId=-2,
    lastJumpId=-3, possibleJumps=[], paramValues=ParamValues(),
    paramShow=[], jumpedCount={}, locationVisitCount={},
    daysPassed=-4, imageName='1', trackName='2', soundName='3',
    aleaState=AleaState(), aleaSeed='4', performedJumps=[])

# noinspection SpellCheckingInspection
FP_CERT = '54eeaeb3288d6a24676ccfbe60a175d8c161872f5f399eb683a83745e01d4448'
FP_CERT_Z = '8e0db68f3802e9448e96044fdcecb341ccfd3e2b987e2155cfb93fdd75689645'


@pytest.fixture
def temp_cert():
    with open(f'{TEST_RESOURCE_DIR}/test-qqqq.crt', 'rb') as cert:
        cert = load_certificate(FILETYPE_PEM, cert.read())
    yield cert
    del cert


@pytest.fixture
def temp_cert_z():
    with open(f'{TEST_RESOURCE_DIR}/test-zzzz.crt', 'rb') as cert:
        cert = load_certificate(FILETYPE_PEM, cert.read())
    yield cert
    del cert


def test_create_anon(temp_db, temp_cert):
    with temp_db.atomic():
        assert not Cert.by(fp_cert=FP_CERT)
        ident = gmcapsule.Identity(temp_cert)
        Ranger.create_anon(ident)

    with temp_db.atomic():
        cert = Cert.by(fp_cert=FP_CERT)
        assert cert
        assert cert.subj == 'qqqq'
        Ranger.create_anon(ident)

    with temp_db.atomic():
        assert Cert.select().count() == 1


def test_opts_lang(temp_db, temp_cert):
    with temp_db.atomic():
        ident = gmcapsule.Identity(temp_cert)
        Ranger.create_anon(ident)
        #
        Options.save_lang(FP_CERT, 'qwe')
        assert Ranger.by(fp_cert=FP_CERT).get_opts().lang == 'qwe'


def test_ip_lang(temp_db):
    with temp_db.atomic():
        assert IpOptions.lang_by_ip('127.0.0.1') == 'en'
        IpOptions.save_lang('127.0.0.1', 'ru')
        assert IpOptions.lang_by_ip('127.0.0.1') == 'ru'


def test_certs(temp_db, temp_cert):
    with temp_db.atomic():
        ident = gmcapsule.Identity(temp_cert)
        Ranger.create_anon(ident)
        #
        cert = Cert.by(fp_cert=FP_CERT)
        anon = Ranger.by(fp_cert=FP_CERT)
        assert anon.get_certs() == [cert]


def test_ranger_exists_case_insensitive(temp_db, temp_cert):
    with temp_db.atomic():
        ident = gmcapsule.Identity(temp_cert)
        Ranger.create_anon(ident)
        ranger = Ranger.by(fp_cert=FP_CERT)
        ranger.name = 'Qwerty'
        ranger.is_anon = False
        ranger.save()
        #
    assert not Ranger.exists_name('Qwertyuiop')
    assert Ranger.exists_name('Qwerty')
    assert Ranger.exists_name('qWERTY')


def test_migrations(temp_db):
    router = Router(temp_db, migrate_dir=MIGRATE_DIR)
    assert Quest.select().count() == 208
    assert Star.select().count() == 144
    assert Planet.select().count() == 1326
    router.rollback()  # 009
    router.rollback()  # 008
    router.rollback()  # 007
    router.rollback()  # 006
    router.rollback()  # 005
    assert Star.select().count() == 0
    assert Planet.select().count() == 0
    router.rollback()  # 004
    router.rollback()  # 003
    router.rollback()  # 002
    assert Quest.select().count() == 0
    router.rollback()  # 001
    router.run()
    assert Quest.select().count() == 208


def test_cert_foreign_key_cascade(temp_db, temp_cert):
    assert Quest.select().count() == 208

    with temp_db.atomic():
        ident = gmcapsule.Identity(temp_cert)
        Ranger.create_anon(ident)
        ranger = Ranger.by(fp_cert=FP_CERT)
        Options.save_lang(FP_CERT, 'ru')
        QuestState.save_state(FP_CERT, 138, 99, GAME_STATE,
                              DEFAULT_PLAYERS['ru'])

    assert QuestState.select().count() == 1
    assert Options.select().count() == 1
    assert len(ranger.get_certs()) == 1
    ranger.delete_instance()
    assert QuestState.select().count() == 0
    assert Options.select().count() == 0
    assert Cert.select().count() == 0


def test_quest_state(temp_db, temp_cert):
    with temp_db.atomic():
        ident = gmcapsule.Identity(temp_cert)
        Ranger.create_anon(ident)
        rid = Ranger.by(fp_cert=FP_CERT).id

    sid, st = QuestState.save_state(FP_CERT, 138, 99, GAME_STATE,
                                    DEFAULT_PLAYERS['ru'])
    assert sid == 99
    assert st == GAME_STATE
    assert QuestState.by(fp_cert=FP_CERT, qid=137) is None
    assert QuestState.by(fp_cert=FP_CERT, qid=138).state == GAME_STATE.to_json()
    assert QuestState.by(fp_cert=FP_CERT, qid=999) is None
    #
    QuestState.del_state_at_the_end(
        PlayerState(text='', gameState=GameStateEnum.running),
        FP_CERT, qid=138, rid=rid)
    assert QuestState.by(fp_cert=FP_CERT, qid=138) is not None
    #
    QuestState.del_state_at_the_end(
        PlayerState(text='', gameState=GameStateEnum.win),
        FP_CERT, qid=138, rid=rid)
    assert QuestState.by(fp_cert=FP_CERT, qid=138) is None
    assert QuestCompleted.by(rid=rid, qid=138) == [138]


def test_quest_completed(temp_db, temp_cert):
    with temp_db.atomic():
        ident = gmcapsule.Identity(temp_cert)
        Ranger.create_anon(ident)
        rid = Ranger.by(fp_cert=FP_CERT).id
        QuestState.save_state(FP_CERT, 138, 99, GAME_STATE,
                              DEFAULT_PLAYERS['ru'])
        QuestCompleted.save_by(rid=rid, qid=137)
        #
    in_progress = QuestState.in_progress(rid=rid)
    assert 138 in in_progress
    assert QuestCompleted.by(rid=rid, qid=138) == []
    assert QuestCompleted.by(rid=rid) == [137]
    assert QuestCompleted.by(rid=rid, qid=137) == [137]


def test_planet_sol(temp_db):
    for _ in range(100):
        planet = Planet.choice_by(lang='en', race=['No'], in_sol=True)
        assert planet.id not in SOL_INHABITED
        assert planet.id in SOL_UNINHABITED

    for _ in range(100):
        planet = Planet.choice_by(lang='en', race=['Ignored'], in_sol=True)
        assert planet.id in SOL_INHABITED
        assert planet.id not in SOL_UNINHABITED


def test_leaders(temp_db, temp_cert, temp_cert_z):
    with temp_db.atomic():
        ident = gmcapsule.Identity(temp_cert)
        Ranger.create_anon(ident)
        qqq = Ranger.by(fp_cert=FP_CERT)
        qqq.is_anon = False
        qqq.name = 'qqqq'
        qqq.credits_ru = 2002
        qqq.credits_en = 5000
        qqq.save()
        #
        QuestCompleted.save_by(rid=qqq, qid=137)  # ru
        QuestCompleted.save_by(rid=qqq, qid=6)  # en
        QuestCompleted.save_by(rid=qqq, qid=11)  # en
        QuestCompleted.save_by(rid=qqq, qid=3)  # en
        #
        ident = gmcapsule.Identity(temp_cert_z)
        Ranger.create_anon(ident)
        zzz = Ranger.by(fp_cert=FP_CERT_Z)
        zzz.is_anon = False
        zzz.name = 'zzzz'
        zzz.credits_ru = 2001
        zzz.credits_en = 4000
        zzz.save()
        #
        QuestCompleted.save_by(rid=zzz, qid=136)  # ru
        QuestCompleted.save_by(rid=zzz, qid=135)  # ru
        QuestCompleted.save_by(rid=zzz, qid=3)  # en

        rows = [r for r in Ranger.leaders(lang='ru')]
        assert 2 == len(rows)
        assert rows[0] == (zzz.id, 'zzzz', 2, 2001)
        assert rows[1] == (qqq.id, 'qqqq', 1, 2002)

        rows = [r for r in Ranger.leaders(lang='en')]
        assert 2 == len(rows)
        assert rows[0] == (qqq.id, 'qqqq', 3, 5000)
        assert rows[1] == (zzz.id, 'zzzz', 1, 4000)
        #
        QuestCompleted.save_by(rid=qqq, qid=135)  # ru
        qqq.save()
        rows = [r for r in Ranger.leaders(lang='ru')]
        assert 2 == len(rows)
        assert rows[0] == (qqq.id, 'qqqq', 2, 2002)  # more credits
        assert rows[1] == (zzz.id, 'zzzz', 2, 2001)

