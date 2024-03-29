import logging

import pytest

from srqmplayer.qmplayer import JUMP_I_AGREE
from srqmplayer.qmplayer.funcs import GameState, GameStateEnum
from tests import create_player_n_jump_agree, jump_to, create_player

log = logging.getLogger()


def test_player_on_test6_empty():
    player = create_player_n_jump_agree('test6-empty.qm')
    save: GameState = player.get_saving()

    log.info('Crit params on loc/jumps')
    player.load_saving(save)  # before each
    log.info('failonloc_chain')
    jump_to(player, 'failonloc_chain')
    assert player.get_state().text == 'p2_at_l11'
    assert player.get_state().gameState == GameStateEnum.fail

    player.load_saving(save)  # before each
    log.info('success_on_loc_jumptext')
    jump_to(player, 'success_on_loc_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'success_on_loc_msg'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    log.info('success_on_loc_no_jumptext')
    jump_to(player, 'success_on_loc_no_jumptext')
    assert player.get_state().text, 'success_on_loc_msg'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    log.info('success_on_locnotext_nojumptext')
    jump_to(player, 'success_on_locnotext_nojumptext')
    assert player.get_state().text, 'p1_at_l10'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    log.info('success_on_locnotext_jumptext')
    jump_to(player, 'success_on_locnotext_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'p1_at_l10'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    log.info('success_on_jump_jumptext')
    jump_to(player, 'success_on_jump_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'success_on_jump_jumptext_msg'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    log.info('success_on_jump_nojumptext')
    jump_to(player, 'success_on_jump_nojumptext')
    assert player.get_state().text == 'success_on_jump_nojumptext_msg'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    log.info('fail_on_jump_jumptext')
    jump_to(player, 'fail_on_jump_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'fail_jump_msg'
    assert player.get_state().gameState == GameStateEnum.fail

    player.load_saving(save)  # before each
    log.info('fail_on_jump_nojumptext')
    jump_to(player, 'fail_on_jump_nojumptext')
    assert player.get_state().text == 'fail_jump_text'
    assert player.get_state().gameState == GameStateEnum.fail

    player.load_saving(save)  # before each
    log.info('fail_on_loc_jumptext')
    jump_to(player, 'fail_on_loc_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'fail_loc_msg'
    assert player.get_state().gameState == GameStateEnum.fail

    player.load_saving(save)  # before each
    log.info('fail_on_loc_nojumptext')
    jump_to(player, 'fail_on_loc_nojumptext')
    assert player.get_state().text == 'fail_loc_msg'
    assert player.get_state().gameState == GameStateEnum.fail

    player.load_saving(save)  # before each
    log.info('fail_on_locnotext_jumptext')
    jump_to(player, 'fail_on_locnotext_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'p2_failed_on_L9'
    assert player.get_state().gameState == GameStateEnum.fail

    player.load_saving(save)  # before each
    log.info('fail_on_locnotext_nojumptext')
    jump_to(player, 'fail_on_locnotext_nojumptext')
    assert player.get_state().text == 'p2_failed_on_L9'
    assert player.get_state().gameState == GameStateEnum.fail

    player.load_saving(save)  # before each
    log.info('death_on_jump_jumptext')
    jump_to(player, 'death_on_jump_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'dead_jump_msg'
    assert player.get_state().gameState == GameStateEnum.dead

    player.load_saving(save)  # before each
    log.info('death_on_jump_nojumptext')
    jump_to(player, 'death_on_jump_nojumptext')
    assert player.get_state().text == 'dead_jump_msg'
    assert player.get_state().gameState == GameStateEnum.dead

    player.load_saving(save)  # before each
    log.info('death_on_loc_jumptext')
    jump_to(player, 'death_on_loc_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'dead_on_loc'
    assert player.get_state().gameState == GameStateEnum.dead

    player.load_saving(save)  # before each
    log.info('death_on_loc_nojumptext')
    jump_to(player, 'death_on_loc_nojumptext')
    assert player.get_state().text == 'dead_on_loc'
    assert player.get_state().gameState == GameStateEnum.dead


def test_player_on_test6():
    player = create_player_n_jump_agree('test6.qm')
    save: GameState = player.get_saving()

    log.info('Crit params on loc/jumps with active jump')
    player.load_saving(save)  # before each
    log.info('success_on_loc_jumptext')
    jump_to(player, 'success_on_loc_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'success_on_loc'
    jump_to(player, '')
    assert player.get_state().text == 'success_on_loc_msg'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    log.info('success_on_loc_no_jumptext')
    jump_to(player, 'success_on_loc_no_jumptext')
    assert player.get_state().text == 'success_on_loc'
    jump_to(player, '')
    assert player.get_state().text == 'success_on_loc_msg'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    log.info('success_on_jump_jumptext')
    jump_to(player, 'success_on_jump_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'success_on_jump_jumptext_msg'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    log.info('success_on_jump_nojumptext')
    jump_to(player, 'success_on_jump_nojumptext')
    assert player.get_state().text == 'success_on_jump_nojumptext_msg'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    log.info('fail_on_jump_jumptext')
    jump_to(player, 'fail_on_jump_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'fail_jump_msg'
    assert player.get_state().gameState == GameStateEnum.fail

    player.load_saving(save)  # before each
    log.info('fail_on_jump_nojumptext')
    jump_to(player, 'fail_on_jump_nojumptext')
    assert player.get_state().text == 'fail_jump_text'
    assert player.get_state().gameState == GameStateEnum.fail

    player.load_saving(save)  # before each
    log.info('fail_on_loc_jumptext live-after-fail')
    jump_to(player, 'fail_on_loc_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'fail_on_loc'
    # Here is live-after-fail
    jump_to(player, '')
    assert player.get_state().text == 'L3'
    assert player.get_state().gameState == GameStateEnum.running

    player.load_saving(save)  # before each
    log.info('fail_on_loc_nojumptext')
    jump_to(player, 'fail_on_loc_nojumptext')
    assert player.get_state().text == 'fail_on_loc'
    # Here is live-after-fail
    jump_to(player, '')
    assert player.get_state().text == 'L3'
    assert player.get_state().gameState == GameStateEnum.running

    player.load_saving(save)  # before each
    log.info('death_on_jump_jumptext')
    jump_to(player, 'death_on_jump_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'dead_jump_msg'
    assert player.get_state().gameState == GameStateEnum.dead

    player.load_saving(save)  # before each
    log.info('death_on_jump_nojumptext')
    jump_to(player, 'death_on_jump_nojumptext')
    assert player.get_state().text == 'dead_jump_msg'
    assert player.get_state().gameState == GameStateEnum.dead

    player.load_saving(save)  # before each
    log.info('death_on_loc_jumptext')
    jump_to(player, 'death_on_loc_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'death_on_loc'
    # Here is live-after-dead
    jump_to(player, '')
    assert player.get_state().text == 'L3'
    assert player.get_state().gameState == GameStateEnum.running

    player.load_saving(save)  # before each
    log.info('death_on_loc_nojumptext')
    jump_to(player, 'death_on_loc_nojumptext')
    assert player.get_state().text == 'death_on_loc'
    # Here is live-after-dead
    jump_to(player, '')
    assert player.get_state().text == 'L3'
    assert player.get_state().gameState == GameStateEnum.running

    log.info('Crit params on loc/jumps without active jump')
    player.load_saving(save)  # before each
    jump_to(player, 'enable_lock')  # before each
    log.info('success_on_loc_jumptext')
    jump_to(player, 'success_on_loc_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'success_on_loc'
    jump_to(player, '')
    assert player.get_state().text == 'success_on_loc_msg'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    jump_to(player, 'enable_lock')  # before each
    log.info('success_on_loc_no_jumptext')
    jump_to(player, 'success_on_loc_no_jumptext')
    assert player.get_state().text == 'success_on_loc'
    jump_to(player, '')
    assert player.get_state().text == 'success_on_loc_msg'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    jump_to(player, 'enable_lock')  # before each
    log.info('success_on_jump_jumptext')
    jump_to(player, 'success_on_jump_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'success_on_jump_jumptext_msg'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    jump_to(player, 'enable_lock')  # before each
    log.info('success_on_jump_nojumptext')
    jump_to(player, 'success_on_jump_nojumptext')
    assert player.get_state().text == 'success_on_jump_nojumptext_msg'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    jump_to(player, 'enable_lock')  # before each
    log.info('fail_on_jump_jumptext')
    jump_to(player, 'fail_on_jump_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'fail_jump_msg'
    assert player.get_state().gameState == GameStateEnum.fail

    player.load_saving(save)  # before each
    jump_to(player, 'enable_lock')  # before each
    log.info('fail_on_jump_nojumptext')
    jump_to(player, 'fail_on_jump_nojumptext')
    assert player.get_state().text == 'fail_jump_text'
    assert player.get_state().gameState == GameStateEnum.fail

    player.load_saving(save)  # before each
    jump_to(player, 'enable_lock')  # before each
    log.info('fail_on_loc_jumptext')
    jump_to(player, 'fail_on_loc_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'fail_on_loc'
    jump_to(player, '')
    assert player.get_state().text == 'fail_loc_msg'
    assert player.get_state().gameState == GameStateEnum.fail

    player.load_saving(save)  # before each
    jump_to(player, 'enable_lock')  # before each
    log.info('fail_on_loc_nojumptext')
    jump_to(player, 'fail_on_loc_nojumptext')
    assert player.get_state().text == 'fail_on_loc'
    jump_to(player, '')
    assert player.get_state().text == 'fail_loc_msg'
    assert player.get_state().gameState == GameStateEnum.fail

    player.load_saving(save)  # before each
    jump_to(player, 'enable_lock')  # before each
    log.info('death_on_jump_jumptext')
    jump_to(player, 'death_on_jump_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'dead_jump_msg'
    assert player.get_state().gameState == GameStateEnum.dead

    player.load_saving(save)  # before each
    jump_to(player, 'enable_lock')  # before each
    log.info('death_on_jump_nojumptext')
    jump_to(player, 'death_on_jump_nojumptext')
    assert player.get_state().text == 'dead_jump_msg'
    assert player.get_state().gameState == GameStateEnum.dead

    player.load_saving(save)  # before each
    jump_to(player, 'enable_lock')  # before each
    log.info('death_on_loc_jumptext')
    jump_to(player, 'death_on_loc_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'death_on_loc'
    jump_to(player, '')
    assert player.get_state().text == 'dead_on_loc'
    assert player.get_state().gameState == GameStateEnum.dead

    player.load_saving(save)  # before each
    jump_to(player, 'enable_lock')  # before each
    log.info('death_on_loc_nojumptext')
    jump_to(player, 'death_on_loc_nojumptext')
    assert player.get_state().text == 'death_on_loc'
    jump_to(player, '')
    assert player.get_state().text == 'dead_on_loc'
    assert player.get_state().gameState == GameStateEnum.dead


def test_player_on_test6_qmm_with_permit_live_after_death_false():
    player = create_player_n_jump_agree('test6.qmm')
    save: GameState = player.get_saving()

    log.info('Crit params on loc/jumps with active jump')
    player.load_saving(save)  # before each
    log.info('success_on_loc_jumptext')
    jump_to(player, 'success_on_loc_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'success_on_loc'
    jump_to(player, '')
    assert player.get_state().text == 'success_on_loc_msg'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    log.info('success_on_loc_no_jumptext')
    jump_to(player, 'success_on_loc_no_jumptext')
    assert player.get_state().text == 'success_on_loc'
    jump_to(player, '')
    assert player.get_state().text == 'success_on_loc_msg'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    log.info('success_on_jump_jumptext')
    jump_to(player, 'success_on_jump_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'success_on_jump_jumptext_msg'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    log.info('success_on_jump_nojumptext')
    jump_to(player, 'success_on_jump_nojumptext')
    assert player.get_state().text == 'success_on_jump_nojumptext_msg'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    log.info('fail_on_jump_jumptext')
    jump_to(player, 'fail_on_jump_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'fail_jump_msg'
    assert player.get_state().gameState == GameStateEnum.fail

    player.load_saving(save)  # before each
    log.info('fail_on_jump_nojumptext')
    jump_to(player, 'fail_on_jump_nojumptext')
    assert player.get_state().text == 'fail_jump_text'
    assert player.get_state().gameState == GameStateEnum.fail

    player.load_saving(save)  # before each
    log.info('fail_on_loc_jumptext')
    jump_to(player, 'fail_on_loc_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'fail_on_loc'
    jump_to(player, '')
    assert player.get_state().text == 'fail_loc_msg'
    assert player.get_state().gameState == GameStateEnum.fail

    player.load_saving(save)  # before each
    log.info('fail_on_loc_nojumptext')
    jump_to(player, 'fail_on_loc_nojumptext')
    assert player.get_state().text == 'fail_on_loc'
    jump_to(player, '')
    assert player.get_state().text == 'fail_loc_msg'
    assert player.get_state().gameState == GameStateEnum.fail

    player.load_saving(save)  # before each
    log.info('death_on_jump_jumptext')
    jump_to(player, 'death_on_jump_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'dead_jump_msg'
    assert player.get_state().gameState == GameStateEnum.dead

    player.load_saving(save)  # before each
    log.info('death_on_jump_nojumptext')
    jump_to(player, 'death_on_jump_nojumptext')
    assert player.get_state().text == 'dead_jump_msg'
    assert player.get_state().gameState == GameStateEnum.dead

    player.load_saving(save)  # before each
    log.info('death_on_loc_jumptext')
    jump_to(player, 'death_on_loc_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'death_on_loc'
    jump_to(player, '')
    assert player.get_state().text == 'dead_on_loc'
    assert player.get_state().gameState == GameStateEnum.dead

    player.load_saving(save)  # before each
    log.info('death_on_loc_nojumptext')
    jump_to(player, 'death_on_loc_nojumptext')
    assert player.get_state().text == 'death_on_loc'
    jump_to(player, '')
    assert player.get_state().text == 'dead_on_loc'
    assert player.get_state().gameState == GameStateEnum.dead


def test_player_on_test5_qm():
    player = create_player('test5.qm')
    log.info('Accept')
    player.perform_jump(JUMP_I_AGREE)
    log.info('In L2')
    assert player.get_state().text == 'L2'


def test_player_on_test5_emptystart_usingformula_qm():
    player = create_player('test5-emptystart-usingformula.qm')
    log.info('Accept')
    player.perform_jump(JUMP_I_AGREE)
    log.info('In L2')
    assert player.get_state().text == 'L2'


def test_player_on_test5_emptystart_usingorder_qm():
    player = create_player('test5-emptystart-usingorder.qm')
    log.info('Accept')
    player.perform_jump(JUMP_I_AGREE)
    log.info('have jump')
    jump_to(player, '')
    log.info('In L2')
    assert player.get_state().text == 'L2'


def test_player_on_test5_emptyloctext_emptyloc_autojump_qm():
    player = create_player('test5-emptyloctext-emptyloc-autojump.qm')

    log.info('Accept')
    player.perform_jump(JUMP_I_AGREE)
    log.info('In L2')
    assert player.get_state().text == 'L2'


def test_test5_emptyloctext_emptyloc_noautojump_qm_doing_1_8():
    #  test5-emptyloctext-emptyloc-noautojump
    # 1_nojumptext_emptyloc_noloctext_jumptext -> "" -> L6
    # 2_jumptext_emptyloc_noloctext_jumptext -> jumptext -> "" -> L6
    # 3_nojumptext_noemptyloc_noloctext_jumptext -> "" -> L6
    # 4_jumptext_noemptyloc_noloctext_jumptext -> jumptext -> "" -> L6
    #
    # 5_nojumptext_emptyloc_loctext_jumptext -> L6
    # 6_jumptext_emptyloc_loctext_jumptext
    # 7_nojumptext_noemptyloc_loctext_jumptext
    # 8_jumptext_noemptyloc_loctext_jumptext

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-noautojump.qm')  # before each

    log.info('1_nojumptext_emptyloc_noloctext_jumptext')
    jump_to(player, '1_nojumptext_emptyloc_noloctext_jumptext')
    assert player.get_state().text == ''
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-noautojump.qm')  # before each
    log.info('2_jumptext_emptyloc_noloctext_jumptext')
    jump_to(player, '2_jumptext_emptyloc_noloctext_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-noautojump.qm')  # before each
    log.info('3_nojumptext_noemptyloc_noloctext_jumptext')
    jump_to(player, '3_nojumptext_noemptyloc_noloctext_jumptext')
    assert player.get_state().text == ''
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-noautojump.qm')  # before each
    log.info('4_jumptext_noemptyloc_noloctext_jumptext')
    jump_to(player, '4_jumptext_noemptyloc_noloctext_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == ''
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-noautojump.qm')  # before each
    log.info('5_nojumptext_emptyloc_loctext_jumptext')
    jump_to(player, '5_nojumptext_emptyloc_loctext_jumptext')
    assert player.get_state().text == 'L10'
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-noautojump.qm')  # before each
    log.info('6_jumptext_emptyloc_loctext_jumptext')
    jump_to(player, '6_jumptext_emptyloc_loctext_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-noautojump.qm')  # before each
    log.info('7_nojumptext_noemptyloc_loctext_jumptext')
    jump_to(player, '7_nojumptext_noemptyloc_loctext_jumptext')
    assert player.get_state().text == 'L11'
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-noautojump.qm')  # before each
    log.info('8_jumptext_noemptyloc_loctext_jumptext')
    jump_to(player, '8_jumptext_noemptyloc_loctext_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'L13'
    jump_to(player, '')
    assert player.get_state().text == 'L6'


def test_player_on_test5_emptyloctext_emptyloc_autojump_qm_doing_9_16():
    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-autojump.qm')  # before each

    log.info('9_nojumptext_emptyloc_noloctext_nojumptext')
    jump_to(player, '9_nojumptext_emptyloc_noloctext_nojumptext')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-autojump.qm')  # before each
    log.info('10_jumptext_emptyloc_noloctext_nojumptext')
    jump_to(player, '10_jumptext_emptyloc_noloctext_nojumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-autojump.qm')  # before each
    log.info('11_nojumptext_noemptyloc_noloctext_nojumptext')
    jump_to(player, '11_nojumptext_noemptyloc_noloctext_nojumptext')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-autojump.qm')  # before each
    log.info('12_jumptext_noemptyloc_noloctext_nojumptext')
    jump_to(player, '12_jumptext_noemptyloc_noloctext_nojumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-autojump.qm')  # before each
    log.info('13_nojumptext_emptyloc_loctext_nojumptext')
    jump_to(player, '13_nojumptext_emptyloc_loctext_nojumptext')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-autojump.qm')  # before each
    log.info('14_jumptext_emptyloc_loctext_nojumptext')
    jump_to(player, '14_jumptext_emptyloc_loctext_nojumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-autojump.qm')  # before each
    log.info('15_nojumptext_noemptyloc_loctext_nojumptext')
    jump_to(player, '15_nojumptext_noemptyloc_loctext_nojumptext')
    assert player.get_state().text == 'L11'
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-autojump.qm')  # before each
    log.info('16_jumptext_noemptyloc_loctext_nojumptext')
    jump_to(player, '16_jumptext_noemptyloc_loctext_nojumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'L13'
    jump_to(player, '')
    assert player.get_state().text == 'L6'


def test_player_on_test5_emptyloctext_emptyloc_noautojump_qmm():
    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-noautojump.qmm')

    # TODO: Fix qmm
    # log.info('Location is empty, but have text, so it is shown')
    # assert player.get_state().text == 'Empry loc with text'
    # jump_to(player, '')
    # assert player.get_state().text == 'L2'


@pytest.mark.skip('TODO: Fix qmm')
def test_player_on_test5_emptyloctext_emptyloc_noautojump_qmm_doing_1_8():
    #  test5-emptyloctext-emptyloc-noautojump
    # 1_nojumptext_emptyloc_noloctext_jumptext -> "" -> L6
    # 2_jumptext_emptyloc_noloctext_jumptext -> jumptext -> "" -> L6
    # 3_nojumptext_noemptyloc_noloctext_jumptext -> "" -> L6
    # 4_jumptext_noemptyloc_noloctext_jumptext -> jumptext -> "" -> L6
    #
    # 5_nojumptext_emptyloc_loctext_jumptext -> L6
    # 6_jumptext_emptyloc_loctext_jumptext
    # 7_nojumptext_noemptyloc_loctext_jumptext
    # 8_jumptext_noemptyloc_loctext_jumptext

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-noautojump.qmm')  # before each
    jump_to(player, '')  # before each

    log.info('1_nojumptext_emptyloc_noloctext_jumptext')
    jump_to(player, '1_nojumptext_emptyloc_noloctext_jumptext')
    assert player.get_state().text == ''  # L2 here in TGE 5.2.9
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-noautojump.qmm')  # before each
    jump_to(player, '')  # before each
    log.info('2_jumptext_emptyloc_noloctext_jumptext')
    jump_to(player, '2_jumptext_emptyloc_noloctext_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-noautojump.qmm')  # before each
    jump_to(player, '')  # before each
    log.info('3_nojumptext_noemptyloc_noloctext_jumptext')
    jump_to(player, '3_nojumptext_noemptyloc_noloctext_jumptext')
    assert player.get_state().text == ''  # L2 here in TGE 5.2.9
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-noautojump.qmm')  # before each
    jump_to(player, '')  # before each
    log.info('4_jumptext_noemptyloc_noloctext_jumptext')
    jump_to(player, '4_jumptext_noemptyloc_noloctext_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == ''  # jumptext here in TGE 5.2.9
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-noautojump.qmm')  # before each
    jump_to(player, '')  # before each
    log.info('5_nojumptext_emptyloc_loctext_jumptext')
    jump_to(player, '5_nojumptext_emptyloc_loctext_jumptext')
    assert player.get_state().text == 'L10'
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-noautojump.qmm')  # before each
    jump_to(player, '')  # before each
    log.info('6_jumptext_emptyloc_loctext_jumptext')
    jump_to(player, '6_jumptext_emptyloc_loctext_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-noautojump.qmm')  # before each
    jump_to(player, '')  # before each
    log.info('7_nojumptext_noemptyloc_loctext_jumptext')
    jump_to(player, '7_nojumptext_noemptyloc_loctext_jumptext')
    assert player.get_state().text == 'L11'
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-noautojump.qmm')  # before each
    jump_to(player, '')  # before each
    log.info('8_jumptext_noemptyloc_loctext_jumptext')
    jump_to(player, '8_jumptext_noemptyloc_loctext_jumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'L13'
    jump_to(player, '')
    assert player.get_state().text == 'L6'


@pytest.mark.skip('TODO: Fix qmm')
def test_player_on_test5_emptyloctext_emptyloc_autojump_qmm_doing_9_16():
    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-autojump.qmm')  # before each
    jump_to(player)
    log.info('9_nojumptext_emptyloc_noloctext_nojumptext')
    jump_to(player, '9_nojumptext_emptyloc_noloctext_nojumptext')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-autojump.qmm')  # before each
    jump_to(player)
    log.info('10_jumptext_emptyloc_noloctext_nojumptext')
    jump_to(player, '10_jumptext_emptyloc_noloctext_nojumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-autojump.qmm')  # before each
    jump_to(player)
    log.info('11_nojumptext_noemptyloc_noloctext_nojumptext')
    jump_to(player, '11_nojumptext_noemptyloc_noloctext_nojumptext')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-autojump.qmm')  # before each
    jump_to(player)
    log.info('12_jumptext_noemptyloc_noloctext_nojumptext')
    jump_to(player, '12_jumptext_noemptyloc_noloctext_nojumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-autojump.qmm')  # before each
    jump_to(player)
    log.info('13_nojumptext_emptyloc_loctext_nojumptext')
    jump_to(player, '13_nojumptext_emptyloc_loctext_nojumptext')
    assert player.get_state().text == 'L10'  # Here is difference between tge4 and tge5
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-autojump.qmm')  # before each
    jump_to(player)
    log.info('14_jumptext_emptyloc_loctext_nojumptext')
    jump_to(player, '14_jumptext_emptyloc_loctext_nojumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-autojump.qmm')  # before each
    jump_to(player)
    log.info('15_nojumptext_noemptyloc_loctext_nojumptext')
    jump_to(player, '15_nojumptext_noemptyloc_loctext_nojumptext')
    assert player.get_state().text == 'L11'
    jump_to(player, '')
    assert player.get_state().text == 'L6'

    player = create_player_n_jump_agree(
        'test5-emptyloctext-emptyloc-autojump.qmm')  # before each
    jump_to(player)
    log.info('16_jumptext_noemptyloc_loctext_nojumptext')
    jump_to(player, '16_jumptext_noemptyloc_loctext_nojumptext')
    assert player.get_state().text == 'jumptext'
    jump_to(player, '')
    assert player.get_state().text == 'L13'
    jump_to(player, '')
    assert player.get_state().text == 'L6'


def test_player_on_test4_qm():
    player = create_player('test4.qm')

    log.info('Accept')
    player.perform_jump(JUMP_I_AGREE)

    log.info('Available jumps')
    log.info('2 jumps available, going first loop')
    jump_to(player, '-> L1')
    assert len(player.get_state().choices) == 3, \
        f'Three jump available {player.get_state()}'

    save = player.get_saving()

    jump_to(player, '-> L8')
    jump_to(player, '-> L9')
    jump_to(player, '-> Start')
    jump_to(player, '-> L8')
    assert not player.get_state().choices, 'Dead end here'
    player.load_saving(save)

    log.info('2 jumps available, going second loop')
    assert len(player.get_state().choices) == 3, 'Three jump available'
    jump_to(player, '-> L2')
    jump_to(player, '-> L3')
    jump_to(player, '-> Start')
    assert len(player.get_state().choices) == 2, 'Two jumps left'

    log.info('2 jumps available, going third loop')
    jump_to(player, '-> L4')
    jump_to(player, '-> L6')
    jump_to(player, '-> L7')
    jump_to(player, '-> L4')
    assert player.get_state().text == 'L4'
    assert len(player.get_state().choices) == 1
    jump_to(player, '')

    log.info('L5')
    assert player.get_state().text == 'L5'
    jump_to(player, '-> L10')
    jump_to(player, '-> L11')
    jump_to(player, '-> L5')
    jump_to(player, '-> L10')
    jump_to(player, '-> L11')
    jump_to(player, '-> L5')
    assert len(player.get_state().choices) == 1
    jump_to(player, '-> L13')

    log.info('L13')
    assert player.get_state().text == 'L13'
    assert len(player.get_state().choices) == 4
    save = player.get_saving()
    jump_to(player, '-> L16')
    assert not player.get_state().choices, 'L16 is dead end'
    player.load_saving(save)
    jump_to(player, '-> L18')
    assert not any(filter(lambda x: x.active, player.get_state().choices)), \
        'L18 is dead end'

    player.load_saving(save)
    jump_to(player, '-> L14')
    jump_to(player, '-> L13')
    jump_to(player, '-> L14')
    jump_to(player, '-> L13')
    assert len(player.get_state().choices) == 3


def test_player_on_test3_qm():
    player = create_player('test3.qm')
    log.info('Accept')
    player.perform_jump(JUMP_I_AGREE)

    log.info('Empty locations/jumps')
    save = player.get_saving()

    player.load_saving(save)  # before each
    log.info('loc0text_0empty_jump0text_param=0')
    jump_to(player, 'loc0text_0empty_jump0text_param=0')
    assert player.get_state().text == 'Main menu', 'Wants main menu'

    player.load_saving(save)  # before each
    log.info('loc0text_0empty_jump0text_param=1')
    # const st =
    jump_to(player, 'loc0text_0empty_jump0text_param=1')
    assert len(player.get_state().choices) == 1
    assert player.get_state().text == ''
    assert jump_to(player, '2win').text == 'Win'

    player.load_saving(save)  # before each
    log.info('loc1text_0empty_jump0text_param=0')
    assert jump_to(player, 'loc1text_0empty_jump0text_param=0').text == 'Text'
    assert len(player.get_state().choices) == 1, 'One choice'

    player.load_saving(save)  # before each
    log.info('loc1text_0empty_jump0text_param=1')
    assert jump_to(player, 'loc1text_0empty_jump0text_param=1').text == 'Text'
    assert len(player.get_state().choices) == 1
    assert jump_to(player, '2win').text == 'Win'

    player.load_saving(save)  # before each
    log.info('loc0text_1empty_jump0text_param=0')
    assert jump_to(player, 'loc0text_1empty_jump0text_param=0'
                   ).text == 'Main menu'

    player.load_saving(save)  # before each
    log.info('loc0loctext1text_1empty_jump0text_param=0')
    assert jump_to(player, 'loc0loctext1text_1empty_jump0text_param=0'
                   ).text == 'Main menu'

    player.load_saving(save)  # before each
    log.info('loc1loctext1text_1empty_jump0text_param=0')
    assert jump_to(player, 'loc1loctext1text_1empty_jump0text_param=0'
                   ).text == 'some_text_l23'
    assert jump_to(player, '').text == 'Main menu'

    player.load_saving(save)  # before each
    log.info('loc0loctext1jumptext1text_1empty_jump0text_param=0')
    assert jump_to(player, 'loc0loctext1jumptext1text_1empty_jump0text_param=0'
                   ).text == 'jump52text'
    assert jump_to(player, '').text == 'Main menu'

    player.load_saving(save)  # before each
    log.info('loc1loctext1jumptext1text_1empty_jump0text_param=0')
    assert jump_to(player, 'loc1loctext1jumptext1text_1empty_jump0text_param=0'
                   ).text == 'jump53text'
    assert jump_to(player, '').text == 'some_text_l23'
    assert jump_to(player, '').text == 'Main menu'

    player.load_saving(save)  # before each
    log.info('loc0text_1empty_jump0text_param=1')
    jump_to(player, 'loc0text_1empty_jump0text_param=1')
    assert len(player.get_state().choices) == 1
    assert jump_to(player, '2win').text == 'Win'

    player.load_saving(save)  # before each
    log.info('loc0text_1empty_jump1text_locparam=0')
    assert jump_to(player, 'loc0text_1empty_jump1text_locparam=0'
                   ).text == 'jumpTextX'
    assert jump_to(player, '').text == 'Main menu'

    player.load_saving(save)  # before each
    log.info('loc0text_1empty_jump1text_locparam=1')
    assert jump_to(player, 'loc0text_1empty_jump1text_locparam=1'
                   ).text == 'jumpText'
    assert len(player.get_state().choices) == 1
    assert jump_to(player, '2win').text == 'Win'

    # TODO:
    #   - Если есть доступные переходы
    #     - fail на критичных параметрах на Провальном типе (так же как на dead)
    #     - критичное успешное выдаёт успех (не как fail/dead)
    #   - Критичный минимум (win/fail/dead)
    #   - Критичные значения на переходе
    #     - ? как в TGE - обрабатывать всегда, или
    #       как в теории - обработать локацию и проверить наличие переходов


def test_player_on_test2_qm():
    player = create_player('test2.qm')
    log.info('Accept')
    player.perform_jump(JUMP_I_AGREE)

    log.info('Main menu')
    assert jump_to(player, 'mainmenu').text == 'Main menu'
    log.info('To equal')
    assert jump_to(player, 'To equal').text == "Here should be 1 jump"
    log.info('Next')
    assert len(player.get_state().choices) == 1
    jump_to(player, 'next')
    assert player.get_state().text == 'Text2'

    log.info('Next')
    assert len(player.get_state().choices) == 1
    jump_to(player, 'next')
    assert player.get_state().text == 'Text3'

    log.info('Main menu')
    assert jump_to(player, 'mainmenu').text == 'Main menu'
    log.info('Save in main menu')
    save = player.get_saving()

    log.info('Ending locations')
    player.load_saving(save)  # before each
    jump_to(player, 'ending_locations')  # before each
    log.info('win0')
    assert jump_to(player, 'win0').text == 'Winner'
    assert jump_to(player, '').gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    jump_to(player, 'ending_locations')  # before each
    log.info('win1')
    assert jump_to(player, 'win1').text == 'text'
    assert jump_to(player, '').text == 'Winner'
    assert jump_to(player, '').gameState == GameStateEnum.win

    player.load_saving(save)  # before each
    jump_to(player, 'ending_locations')  # before each
    log.info('lose0')
    st = jump_to(player, 'lose0')
    assert st.gameState == GameStateEnum.fail and st.text == 'Loser'

    player.load_saving(save)  # before each
    jump_to(player, 'ending_locations')  # before each
    log.info('lose1')
    assert jump_to(player, 'lose1').text == 'text'
    st = jump_to(player, '')
    assert st.gameState == GameStateEnum.fail and st.text == 'Loser'

    player.load_saving(save)  # before each
    jump_to(player, 'ending_locations')  # before each
    log.info('zombie0')
    st = jump_to(player, 'zombie0')
    assert st.gameState == GameStateEnum.dead
    assert st.text == 'Zombie'

    player.load_saving(save)  # before each
    jump_to(player, 'ending_locations')  # before each
    log.info('zombie1')
    assert jump_to(player, 'zombie1').text == 'text'
    st = jump_to(player, '')
    assert st.gameState == GameStateEnum.dead
    assert st.text == 'Zombie'

    log.info('Locations with crit params in update')
    player.load_saving(save)  # before each
    jump_to(player, 'end_by_crit_in_loc')  # before each
    log.info('Fail no zombie')
    jump_to(player, 'failNoZombie')
    assert jump_to(player).gameState == GameStateEnum.dead

    player.load_saving(save)  # before each
    jump_to(player, 'end_by_crit_in_loc')  # before each
    log.info('Fail with zombie')
    jump_to(player, 'failZombie')
    st = jump_to(player)
    assert st.text == 'Zombie'
    assert not st.choices

    log.info('Empty locations/jumps')
    player.load_saving(save)  # before each
    jump_to(player, 'empty_loc_empty_jump')  # before each
    log.info('loc0text_0empty_jump0text_param=0')
    assert jump_to(player, 'loc0text_0empty_jump0text_param=0').text == ''
    assert len(player.get_state().choices) == 1, 'One choice'
    assert not player.get_state().choices[0].active, 'But inactive'
    assert player.get_state().choices[0].text == 'neverActive'

    player.load_saving(save)  # before each
    jump_to(player, 'empty_loc_empty_jump')  # before each
    log.info('loc0text_0empty_jump0text_param=1')
    jump_to(player, 'loc0text_0empty_jump0text_param=1')
    assert len(player.get_state().choices) == 2
    assert jump_to(player, '2win').text == 'Win'

    player.load_saving(save)  # before each
    jump_to(player, 'empty_loc_empty_jump')  # before each
    log.info('loc1text_0empty_jump0text_param=0')
    assert jump_to(player, 'loc1text_0empty_jump0text_param=0').text == 'Text'
    assert len(player.get_state().choices) == 1, 'One choice'
    assert not player.get_state().choices[0].active, 'But inactive'
    assert player.get_state().choices[0].text, 'neverActive'

    player.load_saving(save)  # before each
    jump_to(player, 'empty_loc_empty_jump')  # before each
    log.info('loc1text_0empty_jump0text_param=1')
    assert jump_to(player, 'loc1text_0empty_jump0text_param=1').text == 'Text'
    assert len(player.get_state().choices) == 2
    assert jump_to(player, '2win').text == 'Win'

    player.load_saving(save)  # before each
    jump_to(player, 'empty_loc_empty_jump')  # before each
    log.info('loc0text_1empty_jump0text_param=0')
    assert jump_to(player, 'loc0text_1empty_jump0text_param=0').text == ''
    assert len(player.get_state().choices) == 1, 'One choice'
    assert not player.get_state().choices[0].active, 'But inactive'
    assert player.get_state().choices[0].text == 'neverActive'

    player.load_saving(save)  # before each
    jump_to(player, 'empty_loc_empty_jump')  # before each
    log.info('loc0text_1empty_jump0text_param=1')
    jump_to(player, 'loc0text_1empty_jump0text_param=1')
    assert len(player.get_state().choices) == 2
    assert jump_to(player, '2win').text == 'Win'

    player.load_saving(save)  # before each
    jump_to(player, 'empty_loc_empty_jump')  # before each
    log.info('loc0text_1empty_jump1text_locparam=0')
    assert jump_to(player, 'loc0text_1empty_jump1text_locparam=0'
                   ).text == 'jumpTextX'
    assert len(player.get_state().choices) == 1, 'One choice'
    assert not player.get_state().choices[0].active, 'But inactive'
    assert player.get_state().choices[0].text == 'neverActive'

    player.load_saving(save)  # before each
    jump_to(player, 'empty_loc_empty_jump')  # before each
    log.info('loc0text_1empty_jump1text_locparam=1')
    assert jump_to(player, 'loc0text_1empty_jump1text_locparam=1'
                   ).text == 'jumpText'
    assert len(player.get_state().choices) == 2
    assert jump_to(player, '2win').text, 'Win'

    # TODO:
    #   - Если есть доступные переходы
    #     - fail на критичных параметрах на Провальном типе (так же как на dead)
    #     - критичное успешное выдаёт успех (не как fail/dead)
    #   - Критичный минимум (win/fail/dead)
    #   - Критичные значения на переходе
    #     - ? как в TGE - обрабатывать всегда, или
    #       как в теории - обработать локацию и проверить наличие переходов


def test_player_on_test_qm():
    player = create_player('test.qm')

    log.info('Have first state')
    state1 = player.get_state()
    assert state1.text
    assert state1.gameState == GameStateEnum.running

    log.info('Jumps to accept')
    player.perform_jump(JUMP_I_AGREE)

    log.info('Starting location jumps count')
    state2 = player.get_state()
    # log.info(state2)
    assert len(list(filter(lambda x: x.active, state2.choices))) == 2
    assert len(list(filter(lambda x: not x.active, state2.choices))) == 5

    assert 'p2 / 5' in state2.choices[0].text, 'Choices have p2/5'
    assert 'Видно активен по формуле' in state2.choices[6].text

    log.info('Jumps on jumpId > 2')
    state2 = player.get_state()

    player.perform_jump(list(filter(lambda x: x.jumpId > 2, state2.choices))
                        [0].jumpId)
    state3 = player.get_state()
    # log.info(state3)

    # На описании P10
    player.perform_jump(state3.choices[0].jumpId)

    log.info('Next jumps, hideme param show/hide')
    state4 = player.get_state()
    assert 'hideme' not in state4.paramsState[5]
    # log.info(state4)
    assert state4.text == 'Текст на переходе'

    player.perform_jump(state4.choices[0].jumpId)
    state5 = player.get_state()
    # log.info(state5)
    assert 'hideme' in state5.paramsState[5]

    log.info('Пустая1')
    assert jump_to(player, 'Пустая1').text == 'Пустая1'

    log.info('Пустая 2')
    st7 = jump_to(player, 'Пустая 2')
    assert st7.text == 'Пустая 2 замещенный'
    assert len(st7.choices) == 4

    log.info('Пустой проверка')
    save = player.get_saving()
    st8 = jump_to(player, 'пустой проверка')
    assert st8.text == 'HangsHere'
    assert len(st8.choices) == 1, 'One choice'
    assert not any(filter(lambda x: x.active, st8.choices)), 'Inactive'
    player.load_saving(save)

    log.info('EmptyJumps')
    jump_to(player, 'EmptyJumps')
    jump_to(player, '')
    jump_to(player, '')
    assert player.get_state().text == 'Пустая 2'

    log.info('На тест критичных')
    jump_to(player, 'тест')
    assert player.get_state().text == 'Тест критичных параметров'

    log.info('Делаем сохранение')
    save1 = player.get_saving()

    log.info('OnJumpWithoutDescription')
    jump_to(player, 'OnJumpWithoutDescription')
    assert player.get_state().text == 'CritInJump'
    jump_to(player, '')
    # log.info(player.get_state())
    assert player.get_state().gameState == GameStateEnum.win
    player.load_saving(save1)
    # log.info(f'After load\n\n{player.get_state()}'
    #          f' saved state itself\n\n{save1}')

    log.info('win')
    jump_to(player, 'win')
    assert player.get_state().text == 'YouAreWinner'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win
    player.load_saving(save1)

    log.info('fail')
    jump_to(player, 'fail')
    assert player.get_state().text == 'You failed'
    assert player.get_state().gameState == GameStateEnum.fail
    player.load_saving(save1)

    log.info('dead')
    jump_to(player, 'dead')
    assert player.get_state().text == 'You are dead'
    assert player.get_state().gameState == GameStateEnum.dead
    player.load_saving(save1)

    log.info('OnJumpWithDescription')
    jump_to(player, 'OnJumpWithDescription')
    assert player.get_state().text == 'Blablabla'
    # log.info(f'State = {player.get_saving().state}')
    jump_to(player, '')
    # log.info(f'State = {player.get_saving().state}')
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win
    player.load_saving(save1)

    log.info('Спорные и лимит переходов')
    jump_to(player, 'Спорные')
    jump_to(player, '2times')
    jump_to(player, '2times')
    jump_to(player, '2times')
    jump_to(player, '2times')
    assert len(player.get_state().choices) <= 2

    log.info('Спорные, проверка вероятностей')
    random_jump_count = 0
    for i in range(700):
        # log.info(f'i={i}, f={((i+2) % 3) + 1}'
        #          f' val={int(player.get_state().text)}')
        assert ((i + 2) % 3) + 1 == int(player.get_state().text), \
            'X1'  # + JSON.stringify(player.getSaving(), null, 4));
        random_jump_count += len(list(filter(lambda x: 'random' in x.text,
                                             player.get_state().choices)))
        jump_to(player, 'oooo')
        # log.info(f'~~~~~~~~~~~~~~~~~~~~~~~~~~'
        #          f' i={i} f={((i) % 6) + 3}'
        #          f' state={int(player.get_state().text)}')
        assert (i % 6) + 3 == int(player.get_state().text), 'X2'
        jump_to(player, 'back')

    st10 = player.get_state()
    n4 = int(st10.paramsState[3].replace('<clr>', '').replace('<clrEnd>', ''))
    n5 = int(st10.paramsState[4].replace('<clr>', '').replace('<clrEnd>', ''))
    n6 = int(st10.paramsState[5].replace('<clr>', '').replace('<clrEnd>', ''))
    assert 50 < n4 < 150
    assert 350 < n5 < 450
    assert 150 < n6 < 250
    assert 100 < random_jump_count < 200
    player.load_saving(save1)

    log.info('LocationCritOnEmpty -> ToLocationWhichSetsCritParam-WithoutDesc')
    jump_to(player, 'LocationCritOnEmpty')
    jump_to(player, 'ToLocationWhichSetsCritParam-WithoutDesc')
    assert player.get_state().text == 'That location have crit param'
    assert len(player.get_state().choices) == 1
    jump_to(player, '')
    assert player.get_state().text == 'CritLocationMessage'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win
    player.load_saving(save1)

    log.info('LocationCritOnEmpty -> ToLocationWhichSetsCritParam-WithDesc')
    jump_to(player, 'LocationCritOnEmpty')
    jump_to(player, 'ToLocationWhichSetsCritParam-WithDesc')
    assert player.get_state().text == 'Description'
    assert len(player.get_state().choices) == 1
    jump_to(player, '')
    assert player.get_state().text == 'That location have crit param'
    assert len(player.get_state().choices) == 1
    jump_to(player, '')
    assert player.get_state().text == 'CritLocationMessage'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win
    player.load_saving(save1)

    log.info(
        'LocationCritOnEmpty -> ToEmptyLocationWhichSetsCritParam-WithoutDesc')
    jump_to(player, 'LocationCritOnEmpty')
    # log.info(`State === ` + player.getSaving().state);
    jump_to(player, 'ToEmptyLocationWhichSetsCritParam-WithoutDesc')
    # log.info(`State === ` + player.getSaving().state);
    assert player.get_state().text == 'CritEmptyLocationMessage'
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win
    player.load_saving(save1)

    log.info('LocationCritOnEmpty'
             ' -> ToEmptyLocationWhichSetsCritParam-WithDesc')
    jump_to(player, 'LocationCritOnEmpty')
    jump_to(player, 'ToEmptyLocationWhichSetsCritParam-WithDesc')
    assert player.get_state().text == 'Description'
    assert len(player.get_state().choices) == 1
    jump_to(player, '')
    jump_to(player, '')
    assert player.get_state().gameState == GameStateEnum.win
    player.load_saving(save1)
