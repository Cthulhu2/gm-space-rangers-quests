import string
from typing import Dict

from .player import Player

JUMP_I_AGREE = -1
JUMP_NEXT = -2
JUMP_GO_BACK_TO_SHIP = -3

TEXTS_EN = {'iAgree': 'I agree',
            'next': 'Next',
            'goBackToShip': 'Go back to ship',
            'death': 'The great ranger\'s life was numbered',
            'image': 'Image',
            'track': 'Track',
            'inv': 'Inventory',
            'sound': 'Sound'}

TEXTS_RU = {'iAgree': 'Я берусь за это задание',
            'next': 'Далее',
            'goBackToShip': 'Вернуться на корабль',
            'death': 'Жизнь великого рейнджера была сочтена',
            'image': 'Изображение',
            'track': 'Дорожка',
            'inv': 'Инвентарь',
            'sound': 'Звук'}

MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
             'August', 'September', 'October', 'November', 'December']

MONTHS_RU = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля',
             'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']

DEFAULT_DAYS_TO_PASS_QUEST = 35
DEFAULT_PLAYERS: Dict[str, Player] = {
    'ru': Player(Ranger='Греф', Player='Греф',
                 FromPlanet='Земля', FromStar='Солнце',
                 ToPlanet='Боннасис', ToStar='Процион',
                 Money='10000',
                 months=MONTHS_RU, texts=TEXTS_RU),

    'en': Player(Ranger='Ranger', Player='Ranger',
                 FromPlanet='Earth', FromStar='Sun',
                 ToPlanet='Bonnasis', ToStar='Procyon',
                 Money='10000',
                 months=MONTHS_EN, texts=TEXTS_EN)
}

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
