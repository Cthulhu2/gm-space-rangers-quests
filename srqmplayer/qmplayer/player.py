from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Lang(Enum):
    ru = 'ru'
    en = 'en'


@dataclass
class Player:
    Ranger: str
    Player: str
    Money: str
    FromPlanet: str
    FromStar: str
    ToPlanet: str
    ToStar: str
    lang: Lang
    allowBackButton: Optional[bool]


# TODO: move from this file
DEFAULT_RUS_PLAYER = Player(Ranger='Греф', Player='Греф',
                            FromPlanet='Земля', FromStar='Солнце',
                            ToPlanet='Боннасис', ToStar='Процион',
                            Money='10000',
                            #
                            lang=Lang.ru,
                            allowBackButton=False)

# TODO: move from this file
DEFAULT_ENG_PLAYER = Player(Ranger='Ranger', Player='Ranger',
                            FromPlanet='Earth', FromStar='Sun',
                            ToPlanet='Bonnasis', ToStar='Procyon',
                            Money='10000',
                            #
                            lang=Lang.en,
                            allowBackButton=False)
