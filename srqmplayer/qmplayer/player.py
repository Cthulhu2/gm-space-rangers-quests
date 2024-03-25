from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Lang(Enum):
    rus = 'rus'
    eng = 'eng'


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
                            FromPlanet='Земля',
                            FromStar='Солнечная',
                            ToPlanet='Боннасис',
                            ToStar='Процион',
                            Money='10000',
                            #
                            lang=Lang.rus,
                            allowBackButton=False)

# TODO: move from this file
DEFAULT_ENG_PLAYER = Player(Ranger='Ranger',
                            Player='Player',
                            FromPlanet='FromPlanet',
                            FromStar='FromStar',
                            ToPlanet='ToPlanet',
                            ToStar='ToStar',
                            Money='10000',
                            #
                            lang=Lang.eng,
                            allowBackButton=False)
