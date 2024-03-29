from dataclasses import dataclass, field
from enum import IntEnum, Flag
from typing import Optional, List, Union

HEADER_QM_2 = 0x423a35d2  # 24 parameters
HEADER_QM_3 = 0x423a35d3  # 48 parameters
HEADER_QM_4 = 0x423a35d4  # 96 parameters
HEADER_QMM_6 = 0x423a35d6
HEADER_QMM_7 = 0x423a35d7
HEADER_QMM_7_WITH_OLD_TGE_BEHAVIOUR = 0x69f6bd7
HEADERS_QMM_7 = [HEADER_QMM_7, HEADER_QMM_7_WITH_OLD_TGE_BEHAVIOUR]
HEADERS_QMM = [HEADER_QMM_6, HEADER_QMM_7, HEADER_QMM_7_WITH_OLD_TGE_BEHAVIOUR]
LOCATION_TEXTS = 10


# noinspection NonAsciiCharacters
class PlayerRace(IntEnum):
    Малоки = 1
    Пеленги = 2
    Люди = 4
    Феяне = 8
    Гаальцы = 16


# noinspection NonAsciiCharacters
class PlanetRace(Flag):
    Малоки = 1
    Пеленги = 2
    Люди = 4
    Феяне = 8
    Гаальцы = 16
    Незаселенная = 64


class WhenDone(IntEnum):
    OnReturn = 0
    OnFinish = 1


# noinspection NonAsciiCharacters
class PlayerCareer(IntEnum):
    Торговец = 1
    Пират = 2
    Воин = 4


@dataclass
class QMBase:
    givingRace: int
    whenDone: WhenDone
    planetRace: PlanetRace
    playerCareer: int
    playerRace: int
    defaultJumpCountLimit: any
    hardness: any
    paramsCount: any

    changeLogStr: Optional[str]
    majorVer: Optional[int]
    minorVer: Optional[int]

    screenSizeX: int
    screenSizeY: int
    reputationChange: any
    widthSize: int
    heightSize: int


# noinspection NonAsciiCharacters
class ParamType(IntEnum):
    Обычный = 0
    Провальный = 1
    Успешный = 2
    Смертельный = 3


# noinspection NonAsciiCharacters
class ParamCritType(IntEnum):
    Максимум = 0
    Минимум = 1


@dataclass
class QMParamShowInfoPart:
    from_: int
    to: int
    str: str


@dataclass
class Media:
    img: Optional[str]
    sound: Optional[str]
    track: Optional[str]


@dataclass
class QMParamShowInfo:
    showingInfo: List[QMParamShowInfoPart]


@dataclass
class QMParamIsActive:
    active: bool


@dataclass
class QMParam(Media, QMParamShowInfo, QMParamIsActive):
    min: Union[int, float]
    max: Union[int, float]
    type: ParamType
    showWhenZero: bool
    critType: ParamCritType
    isMoney: bool
    name: str
    starting: str
    critValueString: str


@dataclass
class QMBase3:
    header: int


@dataclass
class QMBase2String:
    ToStar: str
    Parsec: Optional[str]
    Artefact: Optional[str]
    ToPlanet: str
    Date: str
    Money: str
    FromPlanet: str
    FromStar: str
    Ranger: str


@dataclass
class QMBase2:
    strings: QMBase2String
    locationsCount: int
    jumpsCount: int
    successText: str
    taskText: str


# noinspection NonAsciiCharacters
class ParameterShowingType(IntEnum):
    НеТрогать = 0x00
    Показать = 0x01
    Скрыть = 0x02


@dataclass()
class ParameterChange(Media):
    change: int
    isChangePercentage: bool
    isChangeValue: bool
    isChangeFormula: bool
    changingFormula: str
    showingType: ParameterShowingType
    critText: str

    @staticmethod
    def empty():
        return ParameterChange(
            img=None, sound=None, track=None, change=0,
            isChangePercentage=False, isChangeValue=False,
            isChangeFormula=False, changingFormula='', critText='',
            showingType=ParameterShowingType.НеТрогать)


class ParameterChangeType(IntEnum):
    Value = 0x00
    Summ = 0x01
    Percentage = 0x02
    Formula = 0x03


class LocationType(IntEnum):
    Ordinary = 0x00
    Starting = 0x01
    Empty = 0x02
    Success = 0x03
    Faily = 0x04
    Deadly = 0x05


@dataclass
class ParamsChanger:
    paramsChanges: List[ParameterChange]


class JumpId(int):
    _usedIds = []

    def __init__(self, value):
        super(int, value)
        if value in JumpId._usedIds:
            raise Exception(f'Non unique JumpId {value}')
        JumpId._usedIds.append(value)


class LocationId(int):
    _usedIds = []
    value: int

    def __init__(self, value: int):
        super(int, value)
        self.value = value
        if value in LocationId._usedIds:
            raise Exception(f'Non unique LocationId {value}')
        LocationId._usedIds.append(value)

    def __eq__(self, other):
        return self.value == other


@dataclass
class JumpParameterCondition:
    mustFrom: int
    mustTo: int
    mustEqualValues: List[int] = field(default_factory=list)
    mustEqualValuesEqual: bool = False
    mustModValues: List[int] = field(default_factory=list)
    mustModValuesMod: bool = False


@dataclass
class Jump(Media, ParamsChanger):
    priority: float
    dayPassed: bool
    id: int
    fromLocationId: int
    toLocationId: int
    alwaysShow: bool
    jumpingCountLimit: int
    showingOrder: int

    paramsConditions: List[JumpParameterCondition]
    formulaToPass: str
    text: str
    description: str


@dataclass
class Location(ParamsChanger):
    dayPassed: bool
    id: int
    isStarting: bool
    isSuccess: bool
    isFaily: bool
    isFailyDeadly: bool
    isEmpty: bool
    texts: List[str]
    media: List[Media]
    isTextByFormula: bool
    textSelectFormula: str
    maxVisits: int
    locX: int
    locY: int


@dataclass
class QM(QMBase, QMBase2, QMBase3):
    params: List[QMParam]
    locations: List[Location]
    jumps: List[Jump]

    def find_jump(self, jid: int) -> Optional[Jump]:
        return next(filter(lambda x: x.id == jid, self.jumps), None)

    def get_jump(self, jid: int) -> Jump:
        jump = self.find_jump(jid)
        if not jump:
            raise Exception(f'Internal error: no jump id={jid}')
        return jump

    def find_loc(self, lid: int) -> Optional[Location]:
        return next(filter(lambda x: x.id == lid, self.locations), None)

    def get_loc(self, lid: int) -> Location:
        loc = self.find_loc(lid)
        if not loc:
            raise Exception(f'Internal error: no loc id={lid}')
        return loc

    @staticmethod
    def create(base: QMBase, base2: QMBase2, base3: QMBase3,
               params: List[QMParam],
               locations: List[Location],
               jumps: List[Jump]):
        return QM(
            header=base3.header,
            #
            strings=base2.strings,
            locationsCount=base2.locationsCount,
            jumpsCount=base2.jumpsCount,
            successText=base2.successText, taskText=base2.taskText,
            #
            givingRace=base.givingRace,
            whenDone=base.whenDone,
            planetRace=base.planetRace,
            playerCareer=base.playerCareer,
            playerRace=base.playerRace,
            defaultJumpCountLimit=base.defaultJumpCountLimit,
            hardness=base.hardness,
            paramsCount=base.paramsCount,
            changeLogStr=base.changeLogStr,
            majorVer=base.majorVer, minorVer=base.minorVer,
            screenSizeX=base.screenSizeX, screenSizeY=base.screenSizeY,
            reputationChange=base.reputationChange,
            widthSize=base.widthSize, heightSize=base.heightSize,
            #
            params=params, locations=locations, jumps=jumps)
