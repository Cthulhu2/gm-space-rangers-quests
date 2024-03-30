import logging

from srqmplayer.formula import ParamValues
from srqmplayer.qmmodels import QMParamShowInfo, QMParamShowInfoPart
from srqmplayer.qmplayer.player import Lang, PlayerSubstitute
from srqmplayer.substitution import substitute
from tests import pseudo_rnd

PLAYER = PlayerSubstitute(Ranger='MyName',
                          Player='Player',
                          FromPlanet='FromPlanet',
                          FromStar='FromStar',
                          ToPlanet='ToPlanet',
                          ToStar='<ToStar>',
                          Date='Date',
                          Day='Day',
                          Money='Money',
                          CurDate='CurDate',
                          lang=Lang.ru,
                          allowBackButton=None)

TEST = {
    "": "",
    "lol kek": "lol kek",
    "У вас [p3] кредитов": "У вас <clr>30<clrEnd> кредитов",
    "Boo {2+3}": "Boo <clr>5<clrEnd>",
    "Boo {2+[10..20]}": "Boo <clr>17<clrEnd>",
    "Lol <Ranger><Ranger>": "Lol <clr>MyName<clrEnd><clr>MyName<clrEnd>",
    "Special char <ToStar>": "Special char <clr><ToStar><clrEnd>",
    "Diamond <>": "Diamond <clr>20<clrEnd>",
    "Один [d2]": "Один <clr>Фиал<clrEnd>",
    "Один [d2:25]": "Один <clr>Bottle<clrEnd>",
    "Один [d2:10+15]": "Один <clr>Bottle<clrEnd>",
    "Один [d2:{25}]": "Один <clr>Bottle<clrEnd>",
    "Один [d2:{10+15}]": "Один <clr>Bottle<clrEnd>",
    "Один [d2:[p1] + 15]": "Один <clr>Bottle<clrEnd>",
    "Один [d2:{[p1] + 15}]": "Один <clr>Bottle<clrEnd>",
    "Deep [d3]": "Deep <clr>Lol <clr>Param1valueString<clrEnd><clrEnd>",
    "Random [d1:[10..20]]": "Random <clr>Param1valueString<clrEnd>",
    "Random [d1:{[10..20]}]": "Random <clr>Param1valueString<clrEnd>",
    "Spaces [d2: { 6  -    3    }    ] ": "Spaces <clr>Fial<clrEnd> ",
    "Multiple [d1] [d1]":
        "Multiple <clr>Param1valueString<clrEnd>"
        " <clr>Param1valueString<clrEnd>",
    "Incorrect [d] [d1]": "Incorrect [d] <clr>Param1valueString<clrEnd>",
    "Incorrect [d:] [d1]": "Incorrect [d:] <clr>Param1valueString<clrEnd>",
    "Incorrect [d[d1]": "Incorrect [d<clr>Param1valueString<clrEnd>",
    "Incorrect [d:{3+5] [d1]":
        "Incorrect [d:{3+5] <clr>Param1valueString<clrEnd>",
    "Incorrect [d:4+] [d1]": "Incorrect [d:4+] <clr>Param1valueString<clrEnd>",
    "Incorrect [d:4+[[] [d1]":
        "Incorrect [d:4+[[] <clr>Param1valueString<clrEnd>",
    "Unknown param [d666]": "Unknown param <clr>UNKNOWN_PARAM<clrEnd>",
}

log = logging.getLogger()


def test_checking_substitute():
    # TODO: What if [d1] refers [d2] which refers [d1]?
    #       TGE crashes with stack overflow
    for str_, expected in TEST.items():
        rnd = pseudo_rnd([5, 6, 7])
        log.info(f'Substitute \'{str_}\' into \'{expected}\'')
        assert substitute(
            str_=str_, player=PLAYER, param_values=ParamValues([10, 20, 30]),
            param_show_infos=[
                QMParamShowInfo(showingInfo=[
                    QMParamShowInfoPart(from_=0, to=20, str='Param1valueString')
                ]),
                QMParamShowInfo(showingInfo=[
                    QMParamShowInfoPart(from_=0, to=5, str='Fial'),
                    QMParamShowInfoPart(from_=5, to=21, str='Фиал'),
                    QMParamShowInfoPart(from_=21, to=26, str='Bottle'),
                ]),
                QMParamShowInfo(showingInfo=[
                    QMParamShowInfoPart(from_=30, to=30, str='Lol [d1]'),
                ]),
            ], rnd=rnd, diamond_idx=1) == expected
