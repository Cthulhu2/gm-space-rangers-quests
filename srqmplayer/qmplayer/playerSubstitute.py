from dataclasses import dataclass

from srqmplayer.qmplayer.player import Player


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
            ToStar=p.ToStar, lang=p.lang, allowBackButton=p.allowBackButton,
            Date=date, Day=day, CurDate=cur_date)
