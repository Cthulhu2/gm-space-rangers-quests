import string
from typing import Dict

from .player import Player

JUMP_I_AGREE = -1
JUMP_NEXT = -2
JUMP_GO_BACK_TO_SHIP = -3

TEXTS_EN = {'iAgree': 'I agree',
            'next': 'Next',
            'goBackToShip': 'Go back to ship',
            'death': 'The great ranger\'s life has ended',
            'image': 'Image',
            'track': 'Track',
            'inv': 'Inventory',
            'sound': 'Sound'}

TEXTS_RU = {'iAgree': 'Я берусь за это задание',
            'next': 'Далее',
            'goBackToShip': 'Вернуться на корабль',
            'death': 'Жизнь великого рейнджера закончилась',
            'image': 'Изображение',
            'track': 'Дорожка',
            'inv': 'Инвентарь',
            'sound': 'Звук'}

TEXTS_ES = {'iAgree': 'Asumo esta tarea.',
            'next': 'Próximo',
            'goBackToShip': 'Regreso al barco',
            'death': 'La vida del gran guardabosques ha terminado',
            'image': 'Imagen',
            'track': 'Pista',
            'inv': 'Inventario',
            'sound': 'Sonido'}

TEXTS_DE = {'iAgree': 'Ich übernehme diese Aufgabe.',
            'next': 'Nächste',
            'goBackToShip': 'Rückkehr zum Schiff',
            'death': 'Der groe Ranger ist tot',
            'image': 'Bild',
            'track': 'Aufnahme',
            'inv': 'Inventar',
            'sound': 'Schall'}

MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
             'August', 'September', 'October', 'November', 'December']

MONTHS_RU = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля',
             'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']

MONTHS_ES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
             'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

MONTHS_DE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli',
             'August', 'September', 'Oktober', 'November', 'Dezember']

DEFAULT_BALANCE = 2000
DEFAULT_DAYS_TO_PASS_QUEST = 35
DEFAULT_PLAYERS: Dict[str, Player] = {
    'ru': Player(Ranger='Греф', Player='Греф',
                 FromPlanet='Земля', FromStar='Солнце',
                 ToPlanet='Боннасис', ToStar='Процион',
                 Money='2000',
                 months=MONTHS_RU, texts=TEXTS_RU, balance=DEFAULT_BALANCE),

    'en': Player(Ranger='Graefe', Player='Graefe',
                 FromPlanet='Earth', FromStar='Sun',
                 ToPlanet='Bonnasis', ToStar='Procyon',
                 Money='2000',
                 months=MONTHS_EN, texts=TEXTS_EN, balance=DEFAULT_BALANCE),
    'es': Player(Ranger='Graefe', Player='Graefe',
                 FromPlanet='Earth', FromStar='Sun',
                 ToPlanet='Bonnasis', ToStar='Procyon',
                 Money='2000',
                 months=MONTHS_ES, texts=TEXTS_ES, balance=DEFAULT_BALANCE),
    'de': Player(Ranger='Graefe', Player='Graefe',
                 FromPlanet='Earth', FromStar='Sun',
                 ToPlanet='Bonnasis', ToStar='Procyon',
                 Money='2000',
                 months=MONTHS_DE, texts=TEXTS_DE, balance=DEFAULT_BALANCE)
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
