import logging
import math
from os.path import dirname, realpath, join
from random import random
from typing import List, Optional, Union

from srqmplayer.qmmodels import QM
from srqmplayer.qmplayer import JUMP_I_AGREE
from srqmplayer.qmplayer.funcs import QMPlayer
from srqmplayer.qmplayer.player import Lang
from srqmplayer.qmreader import parse

log = logging.getLogger()
TEST_RESOURCE_DIR = f'{dirname(realpath(__file__))}/resources'


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
    player = QMPlayer(qm, Lang.ru)
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
