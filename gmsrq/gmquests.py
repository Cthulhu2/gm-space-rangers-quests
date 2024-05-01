import logging
import re
from dataclasses import dataclass
from os.path import join
from typing import Optional, Tuple
from urllib.parse import parse_qs

import gmcapsule

from gmsrq.config import Config, err_handler
from gmsrq.sqlstore import Ranger, db, Cert
from gmsrq.store import (
    QUEST_CACHE, QUEST_NAMES, load_state, save_state, del_state_at_the_end
)
from srqmplayer.qmplayer.funcs import (
    PlayerState, GameStateEnum, QMPlayer, TEXTS_RUS, TEXTS_ENG
)
from srqmplayer.qmplayer.player import Lang
from srqmplayer.qmreader import parse

log = logging.getLogger()

QUEST_ID = 'qid'
STEP_ID = 'sid'
CHOICE_ID = 'cid'


def cut_colors(text):
    ranges = []
    while clr := re.search(r'<clr>', text):
        text = text[:clr.regs[0][0]] + text[clr.regs[0][1]:]
        clr_end = re.search(r'<clrEnd>|</clr>', text)
        if clr_end:
            text = text[:clr_end.regs[0][0]] + text[clr_end.regs[0][1]:]
            ranges.append((clr.regs[0][0], clr_end.regs[0][0]))
    return ranges, text


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


def style(text: str, ansi: bool = True):
    # replace <fix> twice, to render one new line with preformatted
    # 1 - with new lines,
    # 2 - without new lines,
    text = text.replace('\r\n', '\n') \
        .replace('<fix>\n', '```\n').replace('\n</fix>', '\n```') \
        .replace('<fix>', '```\n').replace('</fix>', '\n```') \
        .replace('<br>', '\n')

    while fmt := find_format_tag(text):
        body = fmt.body
        colors_ranges, body = cut_colors(body)  # to correct padding

        # not colorize -- insert emphasis mark BEFORE padding
        if colors_ranges and not ansi:
            for r in reversed(colors_ranges):
                body = body[:r[1]] + '*' + body[r[1]:]
                body = body[:r[0]] + '*' + body[r[0]:]
        pad = 0
        if fmt.padding == 'left':
            body = f'{body:<{fmt.paddingSize}}'
        elif fmt.padding == 'center':
            orig_body_len = len(body)
            body = f'{body:^{fmt.paddingSize}}'
            pad = int((len(body) - orig_body_len) / 2)
        elif fmt.padding == 'right':
            orig_body_len = len(body)
            body = f'{body:>{fmt.paddingSize}}'
            pad = len(body) - orig_body_len
        # colorize -- insert color marks AFTER padding
        if colors_ranges and ansi:
            for r in reversed(colors_ranges):
                body = body[:r[1] + pad] + '\033[0m' + body[r[1] + pad:]
                body = body[:r[0] + pad] + '\033[38;5;11m' + body[r[0] + pad:]
        # insert padded and colorized body
        text = text[:fmt.beginIdx] + body + text[fmt.endIdx:]

    # simple colorize replace AFTER formatted
    if ansi:
        text = text.replace('<clr>', '\033[38;5;11m') \
            .replace('<clrEnd>', '\033[0m') \
            .replace('</clr>', '\033[0m')
    else:
        text = text.replace('<clr>', '*') \
            .replace('<clrEnd>', '*') \
            .replace('</clr>', '*')
    return text


def render_page(cfg: Config, qid: int, sid: int,
                state: PlayerState, lang: Lang,
                ansi: bool = False) -> str:
    texts = TEXTS_RUS if lang == Lang.ru else TEXTS_ENG
    img = ''
    if state.imageName:
        img = state.imageName.lower()
        if not img.endswith('.jpg'):
            img += '.jpg'
        img = f'=> {cfg.img_url}{img} {texts["image"]} ({img})\n'

    track = f'=> {cfg.track_url}{state.trackName.lower()}' \
            f' {texts["track"]} ({state.trackName.lower()})\n' \
        if state.trackName else ''

    snd = f'=> {cfg.snd_url}{state.soundName.lower()}' \
          f' {texts["sound"]} ({state.soundName.lower()})\n' \
        if state.soundName else ''

    text = style(state.text, ansi)

    inventory = '\n'.join(map(
        lambda p: style(p.replace('<fix>', '').replace('</fix>', ''), ansi),
        filter(lambda p: p, state.paramsState or [])))
    if inventory:
        inventory = f'```{texts["inv"]}\n' \
                    f'{inventory}\n' \
                    f'```\n'

    choices = '\n'.join(list(map(
        lambda x: f'=> {cfg.act_url}'
                  f'?{QUEST_ID}={qid}'
                  f'&{STEP_ID}={sid}'
                  f'&{CHOICE_ID}={x.jumpId}'
                  f' {style(x.text, ansi)}'
        if x.active else style(x.text, ansi),
        state.choices)))

    if not choices and state.gameState == GameStateEnum.fail:
        choices += f'=> /{lang.value} {texts["goBackToShip"]} (fail)'
    if not choices and state.gameState == GameStateEnum.win:
        choices += f'=> /{lang.value} {texts["goBackToShip"]} (win)'
    if not choices and state.gameState == GameStateEnum.dead:
        choices += f'=> /{lang.value} {texts["death"]} (death)'

    return f'# {QUEST_NAMES[qid]}\n' \
           f'{img}{track}{snd}{text}\n{inventory}{choices}'


def parse_query(query: str):
    params = parse_qs(query)
    return (int(params[QUEST_ID][0]) if QUEST_ID in params else None,
            int(params[STEP_ID][0]) if STEP_ID in params else None,
            int(params[CHOICE_ID][0]) if CHOICE_ID in params else None)


class GmQuestsHandler:
    cfg: Config

    def __init__(self, cfg: Config):
        self.cfg = cfg

    def init(self, capsule):
        capsule.add(self.cfg.act_url, self.handle)

    @err_handler
    def handle(self, req: gmcapsule.gemini.Request):
        if not req.identity:
            return 60, 'Ranger certificate required' \
                       ' / Требуется сертификат рейнджера'

        qid, sid, cid = parse_query(req.query)
        if not qid or qid not in QUEST_NAMES:
            return 50, f'Unknown quest id={qid}'

        with db.atomic():
            ident: gmcapsule.Identity = req.identity
            Cert.create_anon(ident)
        ranger = Ranger.by(fp_cert=ident.fp_cert)
        player = ranger.name or ident.subject()['CN'] or 'Ranger'

        sid, state, lang = self.process_quest_step(
            player, ident.fp_cert, qid, sid, cid)
        return render_page(self.cfg, qid, sid, state, lang,
                           ranger.get_opts().ansi)

    def process_quest_step(self, player: str, fp_cert: str,
                           qid: int, sid: int, cid: int
                           ) -> Tuple[int, PlayerState, Lang]:
        qm = QUEST_CACHE[qid] if qid in QUEST_CACHE else None
        quest_name = QUEST_NAMES[qid]
        if not qm:
            with open(join(self.cfg.quests_dir, quest_name), 'rb') as f:
                qm = parse(f)
            QUEST_CACHE[qid] = qm
        lang = Lang.en if '_eng.' in quest_name else Lang.ru

        prev_sid, state = load_state(self.cfg.users_dir, fp_cert, quest_name)
        qmplayer = QMPlayer(qm, lang, ranger=player)
        if state:
            qmplayer.load_saving(state)

        if prev_sid != sid or not qmplayer.is_available_jump(cid):
            player_state = qmplayer.get_state()
            return prev_sid, player_state, lang

        qmplayer.perform_jump(cid)
        next_sid = prev_sid + 1
        save_state(self.cfg.users_dir,
                   fp_cert, quest_name, str(next_sid), qmplayer.state)

        player_state = qmplayer.get_state()
        del_state_at_the_end(self.cfg.users_dir,
                             player_state, fp_cert, QUEST_NAMES[qid])
        return next_sid, player_state, lang
