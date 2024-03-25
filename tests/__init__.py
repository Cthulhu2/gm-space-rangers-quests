import logging
from os.path import dirname, realpath, join

from srqmplayer.qmmodels import QM
from srqmplayer.qmplayer import QMPlayer, Lang
from srqmplayer.qmplayer.defs import JUMP_I_AGREE
from srqmplayer.qmreader import parse


log = logging.getLogger()
TEST_RESOURCE_DIR = f'{dirname(realpath(__file__))}/resources'


def jump_to(player: QMPlayer, text: str = ''):
    state = player.get_state()
    jump = next(filter(lambda x: text in x.text and x.active, state.choices),
                None)
    if not jump:
        raise Exception(f'OLOLO: No jump {text} in {state}')
    player.perform_jump(jump.jumpId)
    # console.info(player.getState());
    return player.get_state()


def create_player(quest_filename: str) -> QMPlayer:
    log.info('Reads and parses quest')
    with open(join(TEST_RESOURCE_DIR, quest_filename), 'rb') as f:
        qm: QM = parse(f)
    player = QMPlayer(qm, Lang.rus)
    player.start()
    return player


def create_player_n_jump_agree(quest_filename: str) -> QMPlayer:
    player = create_player(quest_filename)
    player.perform_jump(JUMP_I_AGREE)
    return player
