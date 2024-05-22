from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Player:
    Ranger: str
    Player: str
    Money: str
    FromPlanet: str
    FromStar: str
    ToPlanet: str
    ToStar: str
    #
    months: List[str]
    texts: Dict[str, str]

    def set_planets(self,
                    from_star: str = None, from_planet: str = None,
                    to_star: str = None, to_planet: str = None):
        self.FromStar = from_star or self.FromStar
        self.FromPlanet = from_planet or self.FromPlanet
        self.ToStar = to_star or self.ToStar
        self.ToPlanet = to_planet or self.ToPlanet


@dataclass
class PlayerSubstitute(Player):
    # Дата дедлайна
    Date: str
    # Кол-во дней
    Day: str
    # Текущая дата
    CurDate: str

    @staticmethod
    def of(p: Player, date, day, cur_date):
        return PlayerSubstitute(
            Ranger=p.Ranger, Player=p.Player, Money=p.Money,
            FromPlanet=p.FromPlanet, FromStar=p.FromStar, ToPlanet=p.ToPlanet,
            ToStar=p.ToStar, months=p.months, texts=p.texts,
            Date=date, Day=day, CurDate=cur_date)
