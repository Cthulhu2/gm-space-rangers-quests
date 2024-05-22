import dataclasses
import logging
from datetime import datetime
from os.path import join
from typing import cast

from srqmplayer.qmplayer import JUMP_I_AGREE, JUMP_GO_BACK_TO_SHIP, \
    DEFAULT_PLAYERS
from srqmplayer.qmplayer.funcs import (
    State, get_ui_state, GameStateEnum,
    perform_jump, init_game, Quest, GameLog, GameState
)
from srqmplayer.qmreader import parse
from tests import TEST_RESOURCE_DIR

log = logging.getLogger()

MY_SEED1 = 'someseed'
MY_SEED2 = 'someseed3'

DT_FMT = '%Y-%m-%dT%H:%M:%S.%fZ'
date1 = datetime.strptime('2018-07-22T22:20:36.761Z', DT_FMT).time()
date2 = datetime.strptime('2018-07-22T22:21:36.761Z', DT_FMT).time()
date3 = datetime.strptime('2018-07-22T22:22:36.761Z', DT_FMT).time()
date4 = datetime.strptime('2018-07-22T22:30:36.761Z', DT_FMT).time()


def get_game_log(state: GameState) -> GameLog:
    return GameLog(aleaSeed=state.aleaSeed, performedJumps=state.performedJumps)


def validate_winning_log(quest: Quest, game_log: GameLog):
    state = init_game(quest, game_log.aleaSeed)
    for jump in game_log.performedJumps:
        ui_state = get_ui_state(quest, state, DEFAULT_PLAYERS['ru'], False)
        if any(filter(lambda x: x.jumpId == jump.jumpId, ui_state.choices)):
            log.info(f'Validate jumping jumpId={jump.jumpId}')
            state = perform_jump(jump.jumpId, quest, state,
                                 jump.dateUnix, False)
        else:
            log.info(f'Validate=false jumpId={jump.jumpId} not found')
            return False

    ui_state = get_ui_state(quest, state, DEFAULT_PLAYERS['ru'])
    if ui_state.gameState != GameStateEnum.win:
        log.info('Validate=false, not a win state')
        return False
    log.info('Validate=true')
    return True


def test_using_save_and_validation_qm_seed_1():
    with open(join(TEST_RESOURCE_DIR, 'saveAndValidation.qm'), 'rb') as f:
        quest: Quest = cast(Quest, parse(f))

    log.info('Reads and parses quest')
    state = init_game(quest, MY_SEED1)
    log.info('That seed have 2 jumps')
    state = perform_jump(JUMP_I_AGREE, quest, state, date1)
    assert len(state.possibleJumps) == 2

    log.info('Jumping')
    state = perform_jump(2, quest, state, date1)
    state = perform_jump(3, quest, state, date1)
    state = perform_jump(6, quest, state, date1)
    assert state.paramValues[0:3] == [8, 5, 1]
    state = perform_jump(JUMP_GO_BACK_TO_SHIP, quest, state, date1)
    assert state.state == State.returnedending
    uistate = get_ui_state(quest, state, DEFAULT_PLAYERS['ru'])
    assert uistate.gameState == GameStateEnum.win

    # log.info('Validating state')
    # assert validateState(quest, state)

    log.info('Validating game log')
    game_log = get_game_log(state)
    assert validate_winning_log(quest, game_log)

    log.info('Partial game log is not validated')
    game_log = get_game_log(state)
    partial_game_log = dataclasses.replace(
        game_log, performedJumps=game_log.performedJumps[0:3])

    assert not validate_winning_log(quest, partial_game_log)


def test_using_save_and_validation_qm_seed_2():
    with open(join(TEST_RESOURCE_DIR, 'saveAndValidation.qm'), 'rb') as f:
        quest: Quest = cast(Quest, parse(f))

    log.info('Reads and parses quest')
    state = init_game(quest, MY_SEED2)
    log.info('That seed have 1 jumps')
    state = perform_jump(JUMP_I_AGREE, quest, state, date1)
    assert len(state.possibleJumps) == 1
