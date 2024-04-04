import logging
import os
import re
from dataclasses import dataclass, replace
from os import listdir
from os.path import join, dirname, realpath
from typing import Dict, Optional, Tuple
from urllib.parse import parse_qs

import gmcapsule

from srqmplayer.qmmodels import QM
from srqmplayer.qmplayer.funcs import (
    GameStateEnum, TEXTS_RUS, TEXTS_ENG, GameState, PlayerState, QMPlayer
)
from srqmplayer.qmplayer.player import Lang
from srqmplayer.qmreader import parse

log = logging.getLogger()

ACTION_URL = '/cgi-quests/action'
IMG_URL = '/quests/img/'
SND_URL = '/quests/snd/'
TRACK_URL = '/quests/track/'
QUEST_ID = 'qid'
STEP_ID = 'sid'
CHOICE_ID = 'cid'

QUEST_DIR = f'{dirname(realpath(__file__))}/borrowed/qm'
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

USERS_DIR = f'{dirname(realpath(__file__))}/users'


def parse_query(query: str):
    params = parse_qs(query)
    return (int(params[QUEST_ID][0]) if QUEST_ID in params else None,
            int(params[STEP_ID][0]) if STEP_ID in params else None,
            int(params[CHOICE_ID][0]) if CHOICE_ID in params else None)


def quests_handler(req: gmcapsule.gemini.Request):
    if not req.identity:
        return 60, 'Ranger certificate required' \
                   ' / Требуется сертификат рейнджера'

    try:
        qid, sid, cid = parse_query(req.query)
        if not qid or qid not in QUEST_NAMES:
            return 50, f'Unknown quest id={qid}'

        ident: gmcapsule.Identity = req.identity
        if 'CN' in ident.subject() and ident.subject()['CN']:
            player = ident.subject()['CN']
        else:
            player = 'Ranger'

        sid, state, lang = process_quest_step(player, ident.fp_cert,
                                              qid, sid, cid)

        return render_gemini_page(qid, sid, state, lang)
    except Exception as ex:
        log.warning(f'{ex}', ex)
        return 50, f'{ex}'


# TODO: Use SQLite to store user session
def load_state(fp_cert, quest_name):
    user_dir = join(USERS_DIR, fp_cert)
    if fp_cert not in listdir(USERS_DIR):
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


def save_state(fp_cert, quest_name, sid, state: GameState):
    user_dir = join(USERS_DIR, fp_cert)
    quest_dir = join(user_dir, quest_name)

    with open(join(quest_dir, 'sid'), 'w') as f:
        f.write(sid)

    with open(join(quest_dir, 'game_state.json'), 'w') as f:
        state_json = state.to_json()
        f.write(state_json)

    return sid, state


def del_state_at_the_end(state: PlayerState, fp_cert, quest_name):
    if state.gameState == GameStateEnum.running:
        return  # do nothing
    user_dir = join(USERS_DIR, fp_cert)
    quest_dir = join(user_dir, quest_name)

    os.remove(join(quest_dir, 'sid'))
    os.remove(join(quest_dir, 'game_state.json'))


def process_quest_step(player: str, fp_cert: str,
                       qid: int, sid: int, cid: int
                       ) -> Tuple[int, PlayerState, Lang]:
    qm = QUEST_CACHE[qid] if qid in QUEST_CACHE else None
    quest_name = QUEST_NAMES[qid]
    if not qm:
        with open(join(QUEST_DIR, quest_name), 'rb') as f:
            qm = parse(f)
        QUEST_CACHE[qid] = qm
    lang = Lang.en if '_eng.' in quest_name else Lang.ru

    prev_sid, state = load_state(fp_cert, quest_name)
    qmplayer = QMPlayer(qm, lang)
    qmplayer.player = replace(qmplayer.player, Ranger=player, Player=player)
    if state:
        qmplayer.load_saving(state)

    if cid is None or sid is None or prev_sid != sid:
        save_state(fp_cert, quest_name, str(prev_sid), qmplayer.state)
        player_state = qmplayer.get_state()
        del_state_at_the_end(player_state, fp_cert, QUEST_NAMES[qid])
        return prev_sid, player_state, lang

    qmplayer.perform_jump(cid)
    next_sid = prev_sid + 1
    save_state(fp_cert, quest_name, str(next_sid), qmplayer.state)

    player_state = qmplayer.get_state()
    del_state_at_the_end(player_state, fp_cert, QUEST_NAMES[qid])
    return next_sid, qmplayer.get_state(), lang


def cut_colors(text):
    color_ranges = []
    while clr := re.search(r'<clr>', text):
        text = text[:clr.regs[0][0]] + text[clr.regs[0][1]:]
        clr_end = re.search(r'<clrEnd>|</clr>', text)
        if clr_end:
            text = text[:clr_end.regs[0][0]] + text[clr_end.regs[0][1]:]
            color_ranges.append((clr.regs[0][0], clr_end.regs[0][0]))
    return color_ranges, text


@dataclass
class FormatToken:
    beginIdx: int
    endIdx: int
    body: str
    padding: Optional[str]
    paddingSize: Optional[int]


def find_format_tag(text: str) -> Optional[FormatToken]:
    begin = re.search(r'<format=?(left|right|center)?,?(\d+)?>', text)
    if not begin:
        return None

    end = re.search(r'</format>', text)
    if not end:
        end = re.search(r'$', text)  # end of text

    return FormatToken(beginIdx=begin.regs[0][0],
                       endIdx=end.regs[0][1],
                       body=text[begin.regs[0][1]:end.regs[0][0]],
                       padding=begin[1] if begin[1] else None,
                       paddingSize=int(begin[2]) if begin[2] else 0)


def style(text: str, colorize: bool = True):
    # TODO: Tokenize string and pad nested tags properly
    # replace <fix> twice, to render one new line with preformatted
    # 1 - with new lines,
    # 2 - without new lines,
    text = text.replace('\r\n', '\n') \
        .replace('<fix>\n', '```\n') \
        .replace('\n</fix>', '\n```') \
        .replace('<fix>', '```\n') \
        .replace('</fix>', '\n```') \
        .replace('<br>', '\n')

    while fmt := find_format_tag(text):
        body = fmt.body
        colors_ranges, body = cut_colors(body)  # to correct padding

        # not colorize -- insert emphasis mark BEFORE padding
        if colors_ranges and not colorize:
            for r in reversed(colors_ranges):
                body = body[:r[1]] + '*' + body[r[1]:]
                body = body[:r[0]] + '*' + body[r[0]:]
        if fmt.padding == 'left':
            body = f'{body:<{fmt.paddingSize}}'
            # colorize -- insert color marks AFTER padding
            if colors_ranges and colorize:
                for r in reversed(colors_ranges):
                    body = body[:r[1]] + '\033[0m' + body[r[1]:]
                    body = body[:r[0]] + '\033[38;5;11m' + body[r[0]:]
        elif fmt.padding == 'center':
            orig_body_len = len(body)
            body = f'{body:^{fmt.paddingSize}}'
            # colorize -- insert color marks AFTER padding
            if colors_ranges and colorize:
                pad_len = len(body) - orig_body_len
                pad_len_right = int(pad_len / 2)
                for r in reversed(colors_ranges):
                    body = (body[:r[1] + pad_len_right] + '\033[0m'
                            + body[r[1] + pad_len_right:])
                    body = (body[:r[0] + pad_len_right] + '\033[38;5;11m'
                            + body[r[0] + pad_len_right:])
        elif fmt.padding == 'right':
            orig_body_len = len(body)
            body = f'{body:>{fmt.paddingSize}}'
            # colorize -- insert color marks AFTER padding
            if colors_ranges and colorize:
                pad_len = len(body) - orig_body_len
                for r in reversed(colors_ranges):
                    body = (body[:r[1] + pad_len] + '\033[0m'
                            + body[r[1] + pad_len:])
                    body = (body[:r[0] + pad_len] + '\033[38;5;11m'
                            + body[r[0] + pad_len:])

        # insert padded and colorized body
        text = text[:fmt.beginIdx] + body + text[fmt.endIdx:]

    # simple colorize replace AFTER formatted
    if colorize:
        text = text.replace('<clr>', '\033[38;5;11m') \
            .replace('<clrEnd>', '\033[0m') \
            .replace('</clr>', '\033[0m')
    else:
        text = text.replace('<clr>', '*') \
            .replace('<clrEnd>', '*') \
            .replace('</clr>', '*')
    return text


def render_gemini_page(qid: int, sid: int, state: PlayerState,
                       lang: Lang) -> str:
    texts = TEXTS_RUS if lang == Lang.ru else TEXTS_ENG
    img = ''
    if state.imageName:
        img = state.imageName.lower()
        if not img.endswith('.jpg'):
            img += '.jpg'
        img = f'=> {IMG_URL}{img} {texts["image"]} ({img})\n'

    track = f'=> {TRACK_URL}{state.trackName.lower()}' \
            f' {texts["track"]} ({state.trackName.lower()})\n' \
        if state.trackName else ''

    snd = f'=> {SND_URL}{state.soundName.lower()}' \
          f' {texts["sound"]} ({state.soundName.lower()})\n' \
        if state.soundName else ''

    text = style(state.text)

    inventory = '\n'.join(map(lambda p: style(p.replace('<fix>', '')
                                              .replace('</fix>', '')),
                              filter(lambda p: p, state.paramsState or [])))
    if inventory:
        inventory = f'```{texts["inv"]}\n' \
                    f'{inventory}\n' \
                    f'```\n'

    choices = '\n'.join(list(map(
        lambda x: f'=> {ACTION_URL}?qid={qid}&sid={sid}&cid={x.jumpId}'
                  f' {style(x.text)}'
        if x.active else style(x.text),
        state.choices)))

    if not choices and state.gameState == GameStateEnum.fail:
        choices += f'=> /{lang.value} {texts["goBackToShip"]} (fail)'
    if not choices and state.gameState == GameStateEnum.win:
        choices += f'=> /{lang.value} {texts["goBackToShip"]} (win)'
    if not choices and state.gameState == GameStateEnum.dead:
        choices += f'=> /{lang.value} {texts["death"]} (death)'

    return f'{img}{track}{snd}{text}\n{inventory}{choices}'


def init(capsule: gmcapsule.Context):
    """Extension module initialization."""
    capsule.add(ACTION_URL, quests_handler)


# Local GmCapsule for testing
# TODO: Make gmcapsule pytest-able
if __name__ == "__main__":
    cfg = gmcapsule.Config('./config-local.ini')
    gmcapsule.Capsule(cfg).run()
