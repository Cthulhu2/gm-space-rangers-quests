from datetime import timedelta, datetime
import hashlib
import hmac
import os
from os import listdir
from os.path import join, isfile, islink
from pathlib import Path
from typing import Dict, Optional

import gmcapsule
from OpenSSL.crypto import load_certificate, FILETYPE_ASN1, X509

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


def get_username(users_dir: str, fp_cert: str):
    user_dir = join(users_dir, fp_cert)
    if islink(user_dir):
        return Path(user_dir).resolve().name
    else:
        return None


def get_user_certs(users_dir: str, username: str):
    if username:
        certs = [c.name for c in Path(users_dir).iterdir()
                 if islink(c) and c.resolve().name == username]
        return certs
    else:
        return None


def del_user_cert(users_dir: str, fp_cert: str):
    user_dir = join(users_dir, fp_cert)
    if islink(user_dir):
        os.unlink(user_dir)


def get_cert_info(users_dir: str, fp_cert: str):
    user_dir = join(users_dir, fp_cert)
    cert_info = join(user_dir, f'{fp_cert}.info')

    if isfile(cert_info):
        with open(cert_info, 'r') as f:
            cn = f.readline().strip()
            not_after = f.readline().strip()
            not_after = datetime.strptime(not_after, '%Y%m%d%H%M%SZ')
        return cn, not_after
    return None


def save_cert_info(users_dir: str, ident: gmcapsule.Identity):
    cn = ident.subject()['CN'] if 'CN' in ident.subject() else 'None'
    cert: X509 = load_certificate(FILETYPE_ASN1, ident.cert)
    user_dir = join(users_dir, ident.fp_cert)
    with open(join(user_dir, f'{ident.fp_cert}.info'), 'w') as f:
        f.write(cn)
        f.write('\n')
        f.write(cert.get_notAfter().decode('ascii'))


def get_pass_expires(users_dir: str, username: str) -> Optional[datetime]:
    if not username:
        return None
    user_dir = join(users_dir, username)
    pw_ts = join(user_dir, 'pw.ts')
    if isfile(pw_ts):
        with open(pw_ts, 'r') as f:
            return datetime.fromisoformat(f.readline()) + timedelta(minutes=30)
    return None


def is_valid_pass(users_dir: str, username: str, password: str) -> bool:
    user_dir = join(users_dir, username)
    try:
        with open(join(user_dir, 'pw.hash'), 'rb') as f:
            pw_hash = f.read()
        with open(join(user_dir, 'pw.salt'), 'rb') as f:
            salt = f.read()
        with open(join(user_dir, 'pw.ts'), 'r') as f:
            when = datetime.fromisoformat(f.readline())
    except Exception as ex:
        return False

    if (when + timedelta(minutes=30)) < datetime.utcnow():
        return False

    return hmac.compare_digest(
        pw_hash,
        hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    )


def set_pass(users_dir: str, fp_cert: str, password: str):
    user_dir = join(users_dir, fp_cert)
    os.makedirs(user_dir, exist_ok=True)
    pw_hash = join(user_dir, 'pw.hash')
    pw_salt = join(user_dir, 'pw.salt')
    pw_ts = join(user_dir, 'pw.ts')
    if password:
        salt = os.urandom(16)
        sha256 = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        with open(pw_hash, 'wb') as f:
            f.write(sha256)
        with open(pw_salt, 'wb') as f:
            f.write(salt)
        with open(pw_ts, 'w') as f:
            f.write(f'{datetime.utcnow().isoformat()}')
    else:
        if isfile(pw_hash):
            os.remove(pw_hash)
        if isfile(pw_salt):
            os.remove(pw_salt)
        if isfile(pw_ts):
            os.remove(pw_ts)


def save_lang(users_dir: str, fp_cert: str, lang: str):
    user_dir = join(users_dir, fp_cert)
    os.makedirs(user_dir, exist_ok=True)
    with open(join(user_dir, 'lang'), 'w') as f:
        f.write(lang)


def load_lang(users_dir: str, fp_cert):
    lang_file = join(users_dir, fp_cert, 'lang')
    if isfile(lang_file):
        with open(lang_file, 'r') as f:
            return f.readline()
    return 'en'


def save_ansi(users_dir: str, fp_cert, ansi: bool):
    user_dir = join(users_dir, fp_cert)
    os.makedirs(user_dir, exist_ok=True)

    with open(join(user_dir, 'ansi'), 'w') as f:
        f.write('1' if ansi else '0')


def load_ansi(users_dir: str, fp_cert):
    ansi_file = join(users_dir, fp_cert, 'ansi')
    if isfile(ansi_file):
        with open(ansi_file, 'r') as f:
            return f.readline().startswith('1')
    return False


# TODO: Use SQLite to store user session
def load_state(users_dir: str, fp_cert, quest_name):
    user_dir = join(users_dir, fp_cert)
    os.makedirs(user_dir, exist_ok=True)

    quest_dir = join(user_dir, quest_name)
    os.makedirs(quest_dir, exist_ok=True)

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
