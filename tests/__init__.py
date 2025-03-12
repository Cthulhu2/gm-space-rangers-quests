import logging
import math
import os
from os.path import dirname, realpath, join
from pathlib import Path
from random import random
from typing import List, Optional, Union

import pytest
from peewee_migrate import Router

from gmsrq import MIGRATE_DIR
from gmsrq.sqlstore import db
from srqmplayer.qmmodels import QM
from srqmplayer.qmplayer import JUMP_I_AGREE, DEFAULT_PLAYERS
from srqmplayer.qmplayer.funcs import QMPlayer
from srqmplayer.qmreader import parse

log = logging.getLogger()
TEST_RESOURCE_DIR = f'{dirname(realpath(__file__))}/resources'
QUEST_DIR = join(TEST_RESOURCE_DIR, '../../borrowed/qm/')
TEMP = f'{dirname(realpath(__file__))}/../.tmp'


@pytest.fixture
def temp_db():
    temp = Path(TEMP)
    temp.mkdir(exist_ok=True)
    [os.remove(x) for x in temp.glob('test.sqlite*')]
    db.init(database=f'{TEMP}/test.sqlite')
    router = Router(db, migrate_dir=MIGRATE_DIR)
    router.run()
    try:
        yield db
    finally:
        db.close()


def jump_to(player: QMPlayer, text: str = ''):
    state = player.get_state()
    jump = next(filter(lambda x: text in x.text and x.active,
                       state.choices), None)
    if not jump:
        raise Exception(f'OLOLO: No jump {text} in {state}')
    player.perform_jump(jump.jumpId)
    # console.info(player.getState());
    return player.get_state()


def create_player(quest_filename: str) -> QMPlayer:
    log.info('Reads and parses quest')
    with open(join(TEST_RESOURCE_DIR, quest_filename), 'rb') as f:
        qm: QM = parse(f)
    player = QMPlayer(qm, DEFAULT_PLAYERS['ru'])
    player.start()
    return player


def create_player_n_jump_agree(quest_filename: str) -> QMPlayer:
    player = create_player(quest_filename)
    player.perform_jump(JUMP_I_AGREE)
    return player


def math_rnd(n: int) -> Union[int, float]:
    return math.floor(random() * n) if n is not None else random()


def pseudo_rnd(rnd_values: List[int]):
    rnd_iterator = iter(rnd_values)

    def deterministic_rnd(n: Optional[int]):
        if n is None:
            raise Exception('todo this test')

        val = next(rnd_iterator, None)
        if val is None:
            raise Exception('Lots of randoms')

        if val >= n:
            raise Exception('Why stored random value is greater?')
        return val

    return deterministic_rnd
