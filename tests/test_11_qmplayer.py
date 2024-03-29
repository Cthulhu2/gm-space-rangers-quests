import logging

import pytest

from srqmplayer.qmplayer import JUMP_GO_BACK_TO_SHIP
from srqmplayer.qmplayer.funcs import GameStateEnum
from tests import jump_to, create_player_n_jump_agree

log = logging.getLogger()


def test_test11_critonlocation_qm():
    qm_filename = 'test11-critonlocation.qm'
    player = create_player_n_jump_agree(qm_filename)  # before each
    log.info('-> L2')
    st = jump_to(player, 'L2')
    assert st.choices[0].jumpId == JUMP_GO_BACK_TO_SHIP, 'It is go back to ship'
    assert len(st.choices) == 1, 'one choice'
    player.perform_jump(JUMP_GO_BACK_TO_SHIP)
    assert player.get_state().gameState == GameStateEnum.win

    player = create_player_n_jump_agree(qm_filename)  # before each
    log.info('-> L4')
    st = jump_to(player, 'L4')
    log.info(st)
    assert st.gameState == GameStateEnum.fail
    assert len(st.choices) == 0, 'no choice'

    player = create_player_n_jump_agree(qm_filename)  # before each
    log.info('-> L5')
    st = jump_to(player, 'L5')
    assert st.gameState == GameStateEnum.dead
    assert len(st.choices) == 0, 'no choice'

    player = create_player_n_jump_agree(qm_filename)  # before each
    log.info('-> L6')
    st = jump_to(player, 'L6')
    assert st.text == 'L6'
    st2 = jump_to(player, '')
    assert st2.gameState == GameStateEnum.fail
    assert len(st2.choices) == 0, 'no choice'

    player = create_player_n_jump_agree(qm_filename)  # before each
    log.info('-> L7')
    st = jump_to(player, 'L7')
    assert st.text == 'L7'
    st2 = jump_to(player, '')
    assert st2.gameState == GameStateEnum.dead
    assert len(st2.choices) == 0, 'no choice'

    player = create_player_n_jump_agree(qm_filename)  # before each
    log.info('-> L8')
    st = jump_to(player, 'L8')
    log.info(st)
    assert st.gameState == GameStateEnum.fail
    assert len(st.choices) == 0, 'no choice'

    player = create_player_n_jump_agree(qm_filename)  # before each
    log.info('-> L10')
    st = jump_to(player, 'L10')
    log.info(st)
    assert st.gameState == GameStateEnum.fail
    assert len(st.choices) == 0, 'no choice'


# noinspection PyRedundantParentheses
@pytest.mark.parametrize(('ext'), ('qm', 'qmm'))
def test_player_on_test10_locationtexts_xx(ext):
    player = create_player_n_jump_agree(f'test10-locationtexts.{ext}')

    log.info('1nd jump to L2')
    assert jump_to(player, '-> L2').text == 'L2-1'

    log.info('1nd back to L1')
    assert jump_to(player, '-> L1').text == 'L1-1'

    log.info('2nd jump to L2')
    assert jump_to(player, '-> L2').text, 'L2-2'

    log.info('2nd back to L1')
    assert jump_to(player, '-> L1').text == 'L1-2'

    log.info('3nd jump to L2')
    assert jump_to(player, '-> L2').text == 'L2-4'

    log.info('3nd back to L1 (no text check here)')
    jump_to(player, '-> L1')
    # qm: L1-1 , qmm : L2-4

    log.info('4nd jump to L2')
    assert jump_to(player, '-> L2').text == 'L2-1'

    log.info('4nd back to L1')
    assert jump_to(player, '-> L1').text == 'L1-4'

    log.info('5nd jump to L2')
    assert jump_to(player, '-> L2').text == 'L2-2'

    log.info('5nd back to L1')
    jump_to(player, '-> L1')
    # qm: L1-1 , qmm : L2-4

    log.info('6nd jump to L2')
    assert jump_to(player, '-> L2').text == 'L2-4'

    log.info('6nd back to L1')
    jump_to(player, '-> L1')
    # qm: L1-2 , qmm : L2-4

    log.info('7nd jump to L2')
    assert jump_to(player, '-> L2').text == 'L2-1'

    log.info('7nd back to L1')
    jump_to(player, '-> L1')
    # qm: L1-2

    # qm: 8 -> L1-1 , 9 -> L1-1, 10 -> L1-4 , 11 -> L1-1 ????


def test_player_on_test10_deadly_loc_qmm():
    player = create_player_n_jump_agree('test10-deadly-loc.qmm')
    save = player.get_saving()

    log.info('Jumping to locations')
    log.info('Going to L5')
    assert len(player.get_state().choices) == 4
    jump_to(player, '-> L5')
    assert len(player.get_state().choices) == 1
    assert player.get_state().text == 'L5'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win
    assert len(player.get_state().choices) == 0

    player.load_saving(save)  # before each
    log.info('Going to L4')
    assert len(player.get_state().choices) == 4
    jump_to(player, '-> L4')
    assert player.get_state().text == 'L4fail'
    assert player.get_state().gameState == GameStateEnum.fail
    assert len(player.get_state().choices) == 0

    player.load_saving(save)  # before each
    log.info('Going to L2')
    assert len(player.get_state().choices) == 4
    jump_to(player, '-> L2')
    assert player.get_state().text == 'L2dead'
    assert player.get_state().gameState == GameStateEnum.dead
    assert len(player.get_state().choices) == 0


def test_player_on_limited_location_qmm():
    player = create_player_n_jump_agree('limitedLocation.qmm')
    log.info('Have 3 jumps')
    assert len(player.get_state().choices) == 3

    log.info('Performing walking loop')
    jump_to(player, 'Start --> LimitedLocation')
    jump_to(player, 'LimitedLocation0 --> Start')
    jump_to(player, 'Start --> LimitedLocation')
    jump_to(player, 'LimitedLocation0 --> Start')

    log.info('Have 1 jump')
    assert len(player.get_state().choices) == 1
    assert player.get_state().choices[0].text == 'Start -> winloc'


def test_player_on_test4_forqmm_qm():
    log.info('Old behaviour')
    player = create_player_n_jump_agree('test4-forqmm.qm')
    log.info('Performing walking loop')
    jump_to(player, '-> L1')
    jump_to(player, '--> L2')
    jump_to(player, '')
    jump_to(player, '')
    jump_to(player, '--> L2')
    jump_to(player, '')
    jump_to(player, '')

    log.info('No jump here')
    assert not player.get_state().choices, 'TGE 4 shows not choices here'

    log.info('New behaviour')
    player = create_player_n_jump_agree('test4-forqmm.qmm')
    log.info('Performing walking loop')
    jump_to(player, '-> L1')
    jump_to(player, '--> L2')
    jump_to(player, '')
    jump_to(player, '')
    jump_to(player, '--> L2')
    jump_to(player, '')
    jump_to(player, '')
    # Why? Why is was here?
    # jumpTo('--> L2')
    # jumpTo('')
    # assert player.get_state().gameState == GameStateEnum.win, \
    #     'TGE 5 allows here to win'
    assert not player.get_state().choices, 'TGE 5.2.9 shows not choices here'


def test_player_on_test8_emptyloc_qmm():
    log.info('New behaviour')
    player = create_player_n_jump_agree('test8-emptyloc.qmm')  # before each
    log.info('-> L2')
    assert jump_to(player, '-> L2').text == 'J2desc'
    assert jump_to(player, '').text == 'j3desc'
    assert jump_to(player, '').text == 'j4desc'
    assert jump_to(player, '').text == 'L4'

    player = create_player_n_jump_agree('test8-emptyloc.qmm')  # before each
    log.info('-> L5')
    assert jump_to(player, '-> L5').text == 'J5desc'
    assert jump_to(player, '').text == 'L4'

    player = create_player_n_jump_agree('test8-emptyloc.qmm')  # before each
    log.info('-> L7')
    assert jump_to(player, '-> L7').text == 'J8Desc'
    assert jump_to(player, '').text == 'L4'

    player = create_player_n_jump_agree('test8-emptyloc.qmm')  # before each
    log.info('-> L9')
    assert jump_to(player, '-> L9').text == 'J11Desc'
    assert jump_to(player, '').text == 'L10'
    assert jump_to(player, '').text == 'L4'


def test_player_on_test9_loop_qm_qm():
    player = create_player_n_jump_agree('test9-loop-qm.qm')
    log.info('L1 -> L1')
    assert jump_to(player, '-> L4').text == 'L1'
    assert jump_to(player, '-> L4').text == 'L1'
    assert jump_to(player, '-> L4').text == 'p1_j6_crit'
    assert jump_to(player, '').gameState == GameStateEnum.win

    # player = create_player_n_jump_agree('test9-loop-qm.qm')
    # log.info('L1 -> L1')
    # assert jump_to(player, '-> L1').text == 'L1'
    # #assert jump_to(player, '-> L1').text == 'L1'
    # log.info(jump_to(player, '-> L1'))
    # log.info(jump_to(player, '-> L1'))
    # #assert jump_to(player, '-> L1').text == 'j1crit'
    # assert jump_to(player, '').gameState == GameStateEnum.win


def test_player_on_test9_loop_qmm():
    player = create_player_n_jump_agree('test9-loop.qmm')
    log.info('L1 -> L1')
    assert jump_to(player, '-> L4').text == 'L1'
    assert jump_to(player, '-> L4').text == 'L1'
    assert jump_to(player, '-> L4').text == 'p1_j6_crit'
    assert jump_to(player, '').gameState == GameStateEnum.win

    player = create_player_n_jump_agree('test9-loop.qmm')
    log.info('L1 -> L1')
    assert jump_to(player, '-> L1').text == 'L1'
    assert jump_to(player, '-> L1').text == 'L1'
    assert jump_to(player, '-> L1').text == 'j1crit'
    assert jump_to(player, '').gameState == GameStateEnum.win
