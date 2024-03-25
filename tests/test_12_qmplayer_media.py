import logging

from tests import create_player_n_jump_agree, jump_to

log = logging.getLogger()


def test_media():
    player = create_player_n_jump_agree('mediatest.qmm')  # before each
    log.info('No media in the beginning')
    assert player.get_state().imageName is None
    assert player.get_state().trackName is None
    assert player.get_state().soundName is None
    
    player = create_player_n_jump_agree('mediatest.qmm')  # before each
    log.info('Media on location')
    st = jump_to(player, 'locMedia')
    assert st.imageName == 'Boat_01'
    assert st.trackName == 'track1'
    assert st.soundName == 'sound1'

    player = create_player_n_jump_agree('mediatest.qmm')  # before each
    log.info('Media on location and go back')
    jump_to(player, 'locMedia')
    st = jump_to(player, 'Back')
    assert st.imageName == 'Boat_01'
    assert st.trackName == 'track1'
    assert st.soundName is None
    
    player = create_player_n_jump_agree('mediatest.qmm')  # before each
    log.info('Media on jump with no description')
    st = jump_to(player, 'jumpMediaNoDesc')
    assert st.imageName == 'Boat_02'
    assert st.trackName == 'track02'
    assert st.soundName == 'sound02'
    
    player = create_player_n_jump_agree('mediatest.qmm')  # before each
    log.info('Media on jump with no description and go back')
    jump_to(player, 'jumpMediaNoDesc')
    st = jump_to(player, 'Back')
    assert st.imageName == 'Boat_02'
    assert st.trackName == 'track02'
    assert st.soundName is None
    
    player = create_player_n_jump_agree('mediatest.qmm')  # before each
    log.info('Media on jump with description')
    st = jump_to(player, 'jumpMediaDesc')
    assert st.imageName == 'Ministry_02'
    assert st.trackName == 'track002'
    assert st.soundName == 'sound002'
    
    player = create_player_n_jump_agree('mediatest.qmm')  # before each
    log.info('Media on jump with description and go back')
    jump_to(player, 'jumpMediaDesc')
    st0 = jump_to(player)
    assert st0.soundName is None
    st = jump_to(player, 'Back')
    assert st.imageName == 'Ministry_02'
    assert st.trackName == 'track002'
    assert st0.soundName is None
    
    player = create_player_n_jump_agree('mediatest.qmm')  # before each
    log.info('Media on critparam own media on jump')
    st = jump_to(player, 'SuccessParamOnJumpMediaOwn')
    assert st.imageName == 'boat_03'
    assert st.trackName == 'track3'
    assert st.soundName == 'sound3'
    
    player = create_player_n_jump_agree('mediatest.qmm')  # before each
    log.info('Media on critparam jump override')
    st = jump_to(player, 'SuccessParamMediaJumpOverride')
    assert st.imageName == 'drugs_00'
    assert st.trackName == 'track05'
    assert st.soundName == 'sound05'
    
    player = create_player_n_jump_agree('mediatest.qmm')  # before each
    log.info('Media on critparam location own')
    st = jump_to(player, 'SuccessParamLocationOwn')
    assert st.imageName == 'boat_03'
    assert st.trackName == 'track3'
    assert st.soundName == 'sound3'
    
    player = create_player_n_jump_agree('mediatest.qmm')  # before each
    log.info('Media on critparam location override')
    st = jump_to(player, 'SuccessParamLocationOverride')
    assert st.imageName == 'drugs_02'
    assert st.trackName == 'track06'
    assert st.soundName == 'sound06'
    
    player = create_player_n_jump_agree('mediatest.qmm')  # before each
    log.info('Media track is cleaned')
    assert jump_to(player, 'locMedia').trackName == 'track1'
    assert jump_to(player, 'Back').trackName == 'track1'
    assert jump_to(player, 'cleanTrack').trackName is None
    assert jump_to(player, 'back').trackName is None
