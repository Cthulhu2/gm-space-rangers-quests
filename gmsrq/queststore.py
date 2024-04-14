import os
from os import listdir
from os.path import join
from typing import Dict, Optional

from srqmplayer.qmmodels import QM
from srqmplayer.qmplayer.funcs import GameState, PlayerState, GameStateEnum

QUEST_CACHE: Dict[int, Optional[QM]] = {}
QUEST_NAMES = {1: 'Amnesia.qmm',
               2: 'Badday.qmm',
               3: 'Badday_eng.qm',
               4: 'Bank.qm',
               5: 'Banket.qmm',
               6: 'Banket_eng.qm',
               7: 'Boat.qm',
               8: 'Bomber.qmm',
               9: 'Bondiana.qm',
               10: 'Borzukhan.qmm',
               11: 'Borzukhan_eng.qmm',
               12: 'Build.qm',
               13: 'Casino.qm',
               14: 'Citadels.qmm',
               15: 'Codebox.qmm',
               16: 'Codebox_eng.qm',
               17: 'Colonization.qmm',
               18: 'Commando.qm',
               19: 'Complex.qmm',
               20: 'Cybersport.qmm',
               21: 'Deadoralive.qmm',
               22: 'Depth.qmm',
               23: 'Depth_eng.qm',
               24: 'Diamond.qm',
               25: 'Diehard.qm',
               26: 'Disk.qmm',
               27: 'Disk_eng.qm',
               28: 'Diver.qmm',
               29: 'Domoclan.qmm',
               30: 'Doomino.qmm',
               31: 'Driver.qmm',
               32: 'Driver_eng.qm',
               33: 'Drugs.qmm',
               34: 'Easywork.qmm',
               35: 'Edelweiss.qmm',
               36: 'Edelweiss_eng.qm',
               37: 'Election.qmm',
               38: 'Election_eng.qm',
               39: 'Elus.qmm',
               40: 'Elus_eng.qmm',
               41: 'Energy.qm',
               42: 'Evidence.qmm',
               43: 'Evidence_eng.qm',
               44: 'Evilgenius.qmm',
               45: 'Examen.qm',
               46: 'Faruk.qmm',
               47: 'Feipsycho.qmm',
               48: 'Filial.qmm',
               49: 'Fishing.qm',
               50: 'Fishingcup.qmm',
               51: 'Fishingcup_eng.qm',
               52: 'Foncers.qmm',
               53: 'Foncers_eng.qm',
               54: 'Forum.qmm',
               55: 'Gaidnet.qmm',
               56: 'Galaxy.qm',
               57: 'Gladiator.qm',
               58: 'GLAVRED.qmm',
               59: 'Gluki.qmm',
               60: 'Gobsaur.qm',
               61: 'Hachball.qm',
               62: 'Ikebana.qm',
               63: 'Jumper.qmm',
               64: 'Jumper_eng.qm',
               65: 'Kiberrazum.qmm',
               66: 'Kidnapped.qmm',
               67: 'Leonardo.qmm',
               68: 'Leonardo_eng.qm',
               69: 'Logic.qmm',
               70: 'Logic_eng.qm',
               71: 'LongLiveTheRanger.qmm',
               72: 'Losthero.qmm',
               73: 'Mafia.qmm',
               74: 'mark05.qmm',
               75: 'Massacri.qmm',
               76: 'Maze.qmm',
               77: 'Megatest.qmm',
               78: 'Menzols.qm',
               79: 'Ministry.qmm',
               80: 'Ministry_eng.qm',
               81: 'Moi.qmm',
               82: 'Murder.qm',
               83: 'Muzon.qmm',
               84: 'Muzon_eng.qm',
               85: 'Newflora.qm',
               86: 'Olympiada.qmm',
               87: 'Olympiada_eng.qm',
               88: 'Pachvarash.qmm',
               89: 'Pachvarash_eng.qm',
               90: 'Park.qmm',
               91: 'Penetrator.qm',
               92: 'Pharaon.qmm',
               93: 'Photorobot.qmm',
               94: 'Pilot.qmm',
               95: 'Pilot_eng.qm',
               96: 'PirateClanPrison.qmm',
               97: 'PirateClanPrison_eng.qm',
               98: 'Piratesnest.qmm',
               99: 'Pizza.qmm',
               100: 'Pizza_eng.qm',
               101: 'Player.qmm',
               102: 'Player_eng.qm',
               103: 'Poroda.qm',
               104: 'Prison.qmm',
               105: 'Prison1.qm',
               106: 'Prison_eng.qm',
               107: 'Proprolog.qmm',
               108: 'Provoda.qmm',
               109: 'Rally.qmm',
               110: 'Rally_eng.qm',
               111: 'Robots.qmm',
               112: 'Robots_eng.qm',
               113: 'Rush.qm',
               114: 'Rvk.qmm',
               115: 'Shashki.qmm',
               116: 'Shashki_eng.qm',
               117: 'Sibolusovt.qmm',
               118: 'Sibolusovt_eng.qm',
               119: 'Siege.qm',
               120: 'Ski.qmm',
               121: 'Ski_eng.qm',
               122: 'Sortirovka1.qmm',
               123: 'Sortirovka1_eng.qm',
               124: 'SpaceLines.qmm',
               125: 'SpaceLines_eng.qm',
               126: 'Spy.qm',
               127: 'Stealth.qmm',
               128: 'Stealth_eng.qm',
               129: 'Svarokok.qmm',
               130: 'Svarokok_eng.qm',
               131: 'Taxist.qmm',
               132: 'Testing.qmm',
               133: 'Tomb.qm',
               134: 'Tourists.qmm',
               135: 'Vulkan.qmm',
               136: 'Xenolog.qmm',
               137: 'Xenopark.qmm',
               138: 'Xenopark_eng.qm'}


# TODO: Use SQLite to store user session
def load_state(users_dir: str, fp_cert, quest_name):
    user_dir = join(users_dir, fp_cert)
    if fp_cert not in listdir(users_dir):
        os.makedirs(user_dir)

    quest_dir = join(user_dir, quest_name)
    if quest_name not in listdir(user_dir):
        os.makedirs(quest_dir)

    if 'game_state.json' not in listdir(quest_dir):
        return 0, None  #

    with open(join(quest_dir, 'sid'), 'r') as f:
        sid = int(f.readline())

    with open(join(quest_dir, 'game_state.json'), 'r') as f:
        state_json = f.read()
        state = GameState.from_json(state_json)

    return sid, state


def save_state(users_dir: str, fp_cert, quest_name, sid, state: GameState):
    user_dir = join(users_dir, fp_cert)
    quest_dir = join(user_dir, quest_name)

    with open(join(quest_dir, 'sid'), 'w') as f:
        f.write(sid)

    with open(join(quest_dir, 'game_state.json'), 'w') as f:
        state_json = state.to_json()
        f.write(state_json)

    return sid, state


def del_state_at_the_end(users_dir: str,
                         state: PlayerState, fp_cert, quest_name):
    if state.gameState == GameStateEnum.running:
        return  # do nothing
    user_dir = join(users_dir, fp_cert)
    quest_dir = join(user_dir, quest_name)

    os.remove(join(quest_dir, 'sid'))
    os.remove(join(quest_dir, 'game_state.json'))
