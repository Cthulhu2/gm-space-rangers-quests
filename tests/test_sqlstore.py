import os
from pathlib import Path

import gmcapsule
import pytest
from OpenSSL.crypto import load_certificate, FILETYPE_PEM
from peewee_migrate import Router

from gmsrq.migrations import MIGRATE_DIR
from gmsrq.sqlstore import db, Ranger, Cert, IpOptions, Options, Quest, \
    QuestState
from srqmplayer.alea import AleaState
from srqmplayer.formula import ParamValues
from srqmplayer.qmplayer.funcs import GameState, State, PlayerState, \
    GameStateEnum

# noinspection SpellCheckingInspection
FP_CERT = '54eeaeb3288d6a24676ccfbe60a175d8c161872f5f399eb683a83745e01d4448'


@pytest.fixture
def temp_db():
    [os.remove(x) for x in Path('../.tmp/').glob('test.sqlite*')]
    db.init(database='../.tmp/test.sqlite')
    router = Router(db)
    router.migrate_dir = Path('../gmsrq/migrations')
    router.run()
    return db


@pytest.fixture
def temp_cert():
    with open('test.crt', 'rb') as cert:
        return load_certificate(FILETYPE_PEM, cert.read())


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


def test_migrations(temp_db):
    router = Router(db, migrate_dir=MIGRATE_DIR)
    assert Quest.select().count() == 138
    router.rollback()  # 002
    assert Quest.select().count() == 0
    router.rollback()  # 001
    router.run()
    assert Quest.select().count() == 138


def test_quest_state(temp_db, temp_cert):
    with temp_db.atomic():
        ident = gmcapsule.Identity(temp_cert)
        Ranger.create_anon(ident)
        #
    state = GameState(state=State.starting, critParamId=-1, locationId=-2,
                      lastJumpId=-3, possibleJumps=[],
                      paramValues=ParamValues(), paramShow=[],
                      jumpedCount={}, locationVisitCount={}, daysPassed=-4,
                      imageName='1', trackName='2', soundName='3',
                      aleaState=AleaState(), aleaSeed='4', performedJumps=[])

    sid, st = QuestState.save_state(FP_CERT, 138, 99, state)
    assert sid == 99
    assert st == state
    assert QuestState.by(fp_cert=FP_CERT, qid=137) is None
    assert QuestState.by(fp_cert=FP_CERT, qid=138).state == state.to_json()
    assert QuestState.by(fp_cert=FP_CERT, qid=999) is None
    #
    QuestState.del_state_at_the_end(
        PlayerState(text='', gameState=GameStateEnum.running), FP_CERT, qid=138)
    assert QuestState.by(fp_cert=FP_CERT, qid=138) is not None
    #
    QuestState.del_state_at_the_end(
        PlayerState(text='', gameState=GameStateEnum.fail), FP_CERT, qid=138)
    assert QuestState.by(fp_cert=FP_CERT, qid=138) is None
