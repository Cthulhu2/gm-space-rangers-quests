import string
from random import random
from typing import cast

from srqmplayer.qmmodels import QM
from srqmplayer.qmplayer.funcs import (
    GameState, init_game, Quest,
    PlayerState, get_ui_state, perform_jump
)
from srqmplayer.qmplayer.player import (
    Player, Lang, DEFAULT_RUS_PLAYER, DEFAULT_ENG_PLAYER
)

digs = string.digits + string.ascii_letters


def int2base(x, base):
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)


class QMPlayer:
    quest: QM
    player: Player
    state: GameState

    def __init__(self, quest, lang: Lang):
        self.quest = quest
        self.state = init_game(cast(Quest, quest),
                               int2base(random() * 10_000_000_000, 36))
        self.player = DEFAULT_RUS_PLAYER if lang == Lang.ru \
            else DEFAULT_ENG_PLAYER

    def start(self):
        self.state = init_game(cast(Quest, self.quest),
                               int2base(random() * 10_000_000_000, 36))

    def get_state(self) -> PlayerState:
        return get_ui_state(cast(Quest, self.quest), self.state, self.player)

    def perform_jump(self, jump_id: int):
        self.state = perform_jump(jump_id, cast(Quest, self.quest), self.state)

    def get_saving(self):
        return self.state

    def load_saving(self, state: GameState):
        self.state = state
