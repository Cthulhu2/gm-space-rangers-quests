import io
import logging
import struct
from typing import Optional, List

from srqmplayer.qmmodels import (
    HEADER_QM_2, HEADER_QM_3, HEADER_QM_4, HEADER_QMM_6, HEADER_QMM_7,
    HEADER_QMM_7_WITH_OLD_TGE_BEHAVIOUR, HEADERS_QMM_7, HEADERS_QMM,
    LOCATION_TEXTS, PlanetRace, WhenDone, QMBase,
    ParamType, ParamCritType, QMParamShowInfoPart, Media, QMParam, QMBase3,
    QMBase2String, QMBase2,
    ParameterShowingType, ParameterChange, ParameterChangeType, LocationType,
    JumpParameterCondition, Jump, Location, QM
)

# This is a workaround to tell player to keep old TGE behavior if quest is
# resaved as new version.
# 0x423a35d7 = 1111111127
# 0x69f6bd7  = 0111111127

log = logging.getLogger()


class Reader:
    data: io.BytesIO

    def __init__(self, data: io.BytesIO):
        self.data = data

    def int32(self) -> int:
        read = self.data.read(4)
        return int.from_bytes(read, 'little', signed=True)

    def byte(self) -> int:
        read = self.data.read(1)
        return int.from_bytes(read, 'little')

    def float64(self) -> float:
        read = self.data.read(8)
        unpack = struct.unpack('<d', read)
        return unpack[0]

    def read_string(self, can_be_none: bool = False) -> Optional[str]:
        is_string = self.int32()
        if is_string:
            str_len = self.int32()

            read = self.data.read(str_len * 2)
            val = str(read, 'utf-16-le')
            return val
        else:
            return None if can_be_none else ""

    def seek(self, n: int):
        self.data.seek(n, 1)

    def dword_flag(self, expected: Optional[int] = None):
        val = self.int32()
        if expected is not None and val != expected:
            raise Exception(
                f'Expecting ${expected},'
                f' but get ${val} at position ${self.data.tell() - 4}')

    def is_not_end(self):
        if not self.data.read(1):
            return None
        else:
            self.seek(-1)
            return f'Not an end! We are at 0x{self.data.tell():0x}'


#
#   debugShowHex(n: number = 300) {
#     console.info("Data at 0x" + Number(this.i).toString(16) + "\n");
#     let s = "";
#     for (let i = 0; i < n; i++) {
#       s = s + ("0" + Number(this.data[this.i + i])
#         .toString(16)).slice(-2) + ":";
#       if (i % 16 === 15) {
#         s = s + "\n";
#       }
#     }
#     console.info(s);
#   }
# }


def parse_base(r: Reader, header: int) -> Optional[QMBase]:
    if header in (HEADER_QMM_6, HEADER_QMM_7,
                  HEADER_QMM_7_WITH_OLD_TGE_BEHAVIOUR):
        major_ver = r.int32() if header in HEADERS_QMM_7 else None
        minor_ver = r.int32() if header in HEADERS_QMM_7 else None
        change_log = r.read_string(True) if header in HEADERS_QMM_7 else None

        giving_race = r.byte()
        when_done = WhenDone(r.byte())
        planet_race = PlanetRace(r.byte())
        player_career = r.byte()
        player_race = r.byte()
        reputation_change = r.int32()

        screen_size_x = r.int32()  # In pixels
        screen_size_y = r.int32()  # In pixels
        width_size = r.int32()  # Grid width, from small to big 1E-16-0F-0A
        height_size = r.int32()  # Grid height, from small to big 18-12-0C-08
        default_jump_count_limit = r.int32()
        hardness_ = r.int32()

        params_count = r.int32()

        return QMBase(giving_race, when_done, planet_race, player_career,
                      player_race, default_jump_count_limit, hardness_,
                      params_count, change_log, major_ver, minor_ver,
                      screen_size_x, screen_size_y,
                      reputation_change,
                      width_size, height_size)

    params_count = 48 if header == HEADER_QM_3 \
        else 24 if header == HEADER_QM_2 \
        else 96 if header == HEADER_QM_4 \
        else None
    if not params_count:
        raise Exception(f'Unknown header ${header}')

    r.dword_flag()
    giving_race = r.byte()
    when_done = WhenDone(r.byte())
    r.dword_flag()
    planet_race = PlanetRace(r.byte())
    r.dword_flag()
    player_career = r.byte()
    r.dword_flag()
    player_race = r.byte()
    reputation_change = r.int32()

    screen_size_x = r.int32()
    screen_size_y = r.int32()
    width_size = r.int32()
    height_size = r.int32()
    r.dword_flag()

    default_jump_count_limit = r.int32()
    hardness_ = r.int32()
    return QMBase(giving_race, when_done, planet_race, player_career,
                  player_race, default_jump_count_limit, hardness_,
                  params_count, None, None, None,
                  screen_size_x, screen_size_y,
                  reputation_change,
                  width_size, height_size)


def parse_param(r: Reader) -> QMParam:
    min_ = r.int32()
    max_ = r.int32()
    r.int32()
    type_ = ParamType(r.byte())
    r.int32()
    show_when_zero = bool(r.byte())
    crit_type = ParamCritType(r.byte())
    is_active = bool(r.byte())
    showing_ranges_count = r.int32()
    is_money = bool(r.byte())
    name = r.read_string()

    param: QMParam = QMParam(
        active=is_active, showingInfo=[], img=None, sound=None, track=None,
        min=min_, max=max_, type=type_,
        showWhenZero=show_when_zero, critType=crit_type,
        isMoney=is_money, name=name, starting="", critValueString="")

    for i in range(showing_ranges_count):
        from_ = r.int32()
        to = r.int32()
        str_ = r.read_string()
        param.showingInfo.append(
            QMParamShowInfoPart(from_=from_, to=to, str=str_))

    param.critValueString = r.read_string()
    param.starting = r.read_string()
    return param


def parse_param_qmm(r: Reader) -> QMParam:
    min_ = r.int32()
    max_ = r.int32()
    # console.info(`Param min=${min} max=${max}`)
    type_ = ParamType(r.byte())
    # r.debugShowHex(16);
    unknown1 = r.byte()
    unknown2 = r.byte()
    unknown3 = r.byte()
    if unknown1 != 0:
        log.warning('Unknown1 is params is not zero')
    if unknown2 != 0:
        log.warning('Unknown2 is params is not zero')
    if unknown3 != 0:
        log.warning('Unknown3 is params is not zero')
    show_when_zero = bool(r.byte())
    crit_type = ParamCritType(r.byte())
    is_active = bool(r.byte())
    showing_ranges_count = r.int32()
    is_money = bool(r.byte())
    name = r.read_string()

    param: QMParam = QMParam(is_active, list(), None, None, None,
                             min_, max_, type_, show_when_zero, crit_type,
                             is_money, name, "", "")

    # console.info(`Ranges=${showingRangesCount}`)
    for i in range(showing_ranges_count):
        from_ = r.int32()
        to = r.int32()
        str_ = r.read_string()
        param.showingInfo.append(QMParamShowInfoPart(from_, to, str_))

    param.critValueString = r.read_string()
    param.img = r.read_string(True)
    param.sound = r.read_string(True)
    param.track = r.read_string(True)
    param.starting = r.read_string()
    return param


def parse_base2(r: Reader, is_qmm: bool) -> QMBase2:
    to_star = r.read_string()

    parsec = None if is_qmm else r.read_string(True)
    artefact = None if is_qmm else r.read_string(True)

    to_planet = r.read_string()
    date = r.read_string()
    money = r.read_string()
    from_planet = r.read_string()
    from_star = r.read_string()
    ranger = r.read_string()

    locations_count = r.int32()
    jumps_count = r.int32()

    success_text = r.read_string()

    task_text = r.read_string()

    # noinspection PyUnusedLocal
    unknown_text = None if is_qmm else r.read_string()

    return QMBase2(QMBase2String(to_star, parsec, artefact, to_planet, date,
                                 money, from_planet, from_star, ranger),
                   locations_count, jumps_count, success_text, task_text)


def parse_loc(r: Reader, params_count: int) -> Location:
    day_passed = bool(r.int32())
    loc_x = r.int32()
    loc_y = r.int32()
    id_ = r.int32()
    is_starting = bool(r.byte())
    is_success = bool(r.byte())
    is_faily = bool(r.byte())
    is_faily_deadly = bool(r.byte())
    is_empty = bool(r.byte())

    params_changes: List[ParameterChange] = []
    for i in range(params_count):
        r.seek(12)
        change = r.int32()
        showing_type = ParameterShowingType(r.byte())
        r.seek(4)
        is_change_percentage = bool(r.byte())
        is_change_value = bool(r.byte())
        is_change_formula = bool(r.byte())
        changing_formula = r.read_string()
        r.seek(10)
        crit_text = r.read_string()
        params_changes.append(ParameterChange(
            None, None, None, change,
            is_change_percentage, is_change_value, is_change_formula,
            changing_formula,
            showing_type, crit_text))

    texts: List[str] = []
    media: List[Media] = []
    for i in range(LOCATION_TEXTS):
        texts.append(r.read_string())
        media.append(Media(None, None, None))

    is_text_by_formula = bool(r.byte())
    r.seek(4)
    r.read_string()
    r.read_string()
    text_select_formula = r.read_string()

    return Location(
        id=id_, paramsChanges=params_changes, dayPassed=day_passed,
        isStarting=is_starting, isSuccess=is_success, isEmpty=is_empty,
        isFaily=is_faily, isFailyDeadly=is_faily_deadly,
        texts=texts, media=media,
        isTextByFormula=is_text_by_formula,
        textSelectFormula=text_select_formula,
        maxVisits=0, locX=loc_x, locY=loc_y)


def parse_loc_qmm(r: Reader, params_count: int) -> Location:
    day_passed = bool(r.int32())

    loc_x = r.int32()  # In pixels
    loc_y = r.int32()  # In pixels

    id_ = r.int32()
    max_visits = r.int32()

    type_ = LocationType(r.byte())
    is_starting = type_ == LocationType.Starting
    is_success = type_ == LocationType.Success
    is_faily = type_ == LocationType.Faily
    is_faily_deadly = type_ == LocationType.Deadly
    is_empty = type_ == LocationType.Empty

    params_changes: List[ParameterChange] = []
    for i in range(params_count):
        params_changes.append(ParameterChange.empty())

    affected_params_count = r.int32()
    for i in range(affected_params_count):
        param_num: int = r.int32()

        change = r.int32()
        showing_type = ParameterShowingType(r.byte())
        change_type = ParameterChangeType(r.byte())

        is_change_percentage = change_type == ParameterChangeType.Percentage
        is_change_value = change_type == ParameterChangeType.Value
        is_change_formula = change_type == ParameterChangeType.Formula
        changing_formula = r.read_string()
        crit_text = r.read_string()
        img = r.read_string(True)
        sound = r.read_string(True)
        track = r.read_string(True)

        params_changes[param_num - 1] = ParameterChange(
            img=img, track=track, sound=sound, change=change,
            isChangePercentage=is_change_percentage,
            isChangeValue=is_change_value,
            isChangeFormula=is_change_formula,
            changingFormula=changing_formula,
            showingType=showing_type, critText=crit_text)

    texts: List[str] = []
    media: List[Media] = []
    location_texts = r.int32()
    for i in range(location_texts):
        text = r.read_string()
        texts.append(text)
        img = r.read_string(True)
        sound = r.read_string(True)
        track = r.read_string(True)
        media.append(Media(img=img, track=track, sound=sound))

    is_text_by_formula = bool(r.byte())
    text_select_formula = r.read_string()
    # console.info(is_text_by_formula, text_select_formula)
    # r.debugShowHex(0); // must be 3543
    return Location(
        id=id_, paramsChanges=params_changes, dayPassed=day_passed,
        isStarting=is_starting, isSuccess=is_success, isEmpty=is_empty,
        isFaily=is_faily, isFailyDeadly=is_faily_deadly,
        texts=texts, media=media,
        isTextByFormula=is_text_by_formula,
        textSelectFormula=text_select_formula,
        maxVisits=max_visits, locX=loc_x, locY=loc_y)


def parse_jmp(r: Reader, params_count: int) -> Jump:
    priority_ = r.float64()
    day_passed = bool(r.int32())
    id_ = r.int32()
    from_loc_id = r.int32()
    to_loc_id = r.int32()
    r.seek(1)
    always_show = bool(r.byte())
    jumping_count_limit = r.int32()
    showing_order = r.int32()

    params_changes: List[ParameterChange] = []
    params_conditions: List[JumpParameterCondition] = []
    for i in range(params_count):
        r.seek(4)
        must_from = r.int32()
        must_to = r.int32()
        change = r.int32()
        showing_type = ParameterShowingType(r.int32())
        r.seek(1)
        is_change_percentage = bool(r.byte())
        is_change_value = bool(r.byte())
        is_change_formula = bool(r.byte())
        changing_formula = r.read_string()

        must_equal_values_count = r.int32()
        must_equal_values_equal = bool(r.byte())
        must_equal_values: List[int] = []
        # console.info(`must_equal_values_count=${must_equal_values_count}`)
        for j in range(must_equal_values_count):
            must_equal_values.append(r.int32())
            # console.info('pushed');

        # console.info(`eq=${mustEqualValuesNotEqual}
        #   values = ${must_equal_values.join(', ')}`)
        must_mod_values_count = r.int32()
        # console.info(`must_mod_values_count=${must_mod_values_count}`)
        must_mod_values_mod = bool(r.byte())
        must_mod_values: List[int] = []
        for j in range(must_mod_values_count):
            must_mod_values.append(r.int32())

        crit_text = r.read_string()
        # console.info(`Param ${i} crit text =${crit_text}`)
        params_changes.append(ParameterChange(
            img=None, track=None, sound=None, change=change,
            isChangePercentage=is_change_percentage,
            isChangeValue=is_change_value,
            isChangeFormula=is_change_formula,
            changingFormula=changing_formula,
            showingType=showing_type, critText=crit_text))
        params_conditions.append(JumpParameterCondition(
            mustFrom=must_from, mustTo=must_to,
            mustEqualValues=must_equal_values,
            mustEqualValuesEqual=must_equal_values_equal,
            mustModValues=must_mod_values,
            mustModValuesMod=must_mod_values_mod))

    formula_to_pass = r.read_string()

    text = r.read_string()

    desc = r.read_string()

    return Jump(
        img=None, track=None, sound=None,
        paramsChanges=params_changes,
        priority=priority_, dayPassed=day_passed, id=id_,
        fromLocationId=from_loc_id, toLocationId=to_loc_id,
        alwaysShow=always_show, jumpingCountLimit=jumping_count_limit,
        showingOrder=showing_order, paramsConditions=params_conditions,
        formulaToPass=formula_to_pass, text=text, description=desc)


def parse_jmp_qmm(r: Reader, params_count: int,
                  quest_params: List[QMParam]) -> Jump:
    # r.debugShowHex()
    priority_ = r.float64()
    day_passed = bool(r.int32())
    id_ = r.int32()
    from_loc_id = r.int32()
    to_loc_id = r.int32()

    always_show = bool(r.byte())
    jumping_count_limit = r.int32()
    showing_order = r.int32()

    params_changes: List[ParameterChange] = []
    params_conditions: List[JumpParameterCondition] = []

    for i in range(params_count):
        params_changes.append(ParameterChange.empty())
        params_conditions.append(JumpParameterCondition(
            mustFrom=quest_params[i].min,
            mustTo=quest_params[i].max,
            mustEqualValues=[],
            mustEqualValuesEqual=False,
            mustModValues=[],
            mustModValuesMod=False))

    affected_conditions_params_count = r.int32()
    for i in range(affected_conditions_params_count):
        param_num = r.int32()

        must_from = r.int32()
        must_to = r.int32()

        must_equal_values_count = r.int32()
        must_equal_values_equal = bool(r.byte())
        must_equal_values: List[int] = []
        # console.info(`must_equal_values_count=${must_equal_values_count}`)
        for j in range(must_equal_values_count):
            must_equal_values.append(r.int32())
            #   console.info('pushed')

        must_mod_values_count = r.int32()
        must_mod_values_mod = bool(r.byte())
        must_mod_values: List[int] = []
        for j in range(must_mod_values_count):
            must_mod_values.append(r.int32())

        params_conditions[param_num - 1] = JumpParameterCondition(
            mustFrom=must_from, mustTo=must_to,
            mustEqualValues=must_equal_values,
            mustEqualValuesEqual=must_equal_values_equal,
            mustModValues=must_mod_values,
            mustModValuesMod=must_mod_values_mod)

    affected_change_params_count = r.int32()
    for i in range(affected_change_params_count):
        param_num = r.int32()
        change = r.int32()

        showing_type = ParameterShowingType(r.byte())
        changing_type = ParameterChangeType(r.byte())

        is_change_percentage = changing_type == ParameterChangeType.Percentage
        is_change_value = changing_type == ParameterChangeType.Value
        is_change_formula = changing_type == ParameterChangeType.Formula
        changing_formula = r.read_string()

        crit_text = r.read_string()

        img = r.read_string(True)
        sound = r.read_string(True)
        track = r.read_string(True)

        #  console.info(`Param ${i} crit text =${crit_text}`)
        params_changes[param_num - 1] = ParameterChange(
            img=img, track=track, sound=sound, change=change,
            isChangePercentage=is_change_percentage,
            isChangeValue=is_change_value,
            isChangeFormula=is_change_formula,
            changingFormula=changing_formula,
            showingType=showing_type, critText=crit_text)

    formula_to_pass = r.read_string()

    text = r.read_string()

    desc = r.read_string()
    img = r.read_string(True)
    sound = r.read_string(True)
    track = r.read_string(True)

    return Jump(
        img=img, track=track, sound=sound,
        paramsChanges=params_changes,
        priority=priority_, dayPassed=day_passed, id=id_,
        fromLocationId=from_loc_id, toLocationId=to_loc_id,
        alwaysShow=always_show, jumpingCountLimit=jumping_count_limit,
        showingOrder=showing_order, paramsConditions=params_conditions,
        formulaToPass=formula_to_pass, text=text, description=desc)


def parse(data) -> QM:
    r = Reader(data)
    header = r.int32()

    base = parse_base(r, header)

    is_qmm = header in HEADERS_QMM

    params: List[QMParam] = []
    for i in range(base.paramsCount):
        params.append(parse_param_qmm(r) if is_qmm else parse_param(r))

    base2 = parse_base2(r, is_qmm)

    locations: List[Location] = []
    for i in range(base2.locationsCount):
        locations.append(parse_loc_qmm(r, base.paramsCount) if is_qmm
                         else parse_loc(r, base.paramsCount))

    jumps: List[Jump] = []
    for i in range(base2.jumpsCount):
        jumps.append(parse_jmp_qmm(r, base.paramsCount, params) if is_qmm
                     else parse_jmp(r, base.paramsCount))

    if r.is_not_end():
        raise Exception(r.is_not_end())

    return QM.create(base=base, base2=base2, base3=QMBase3(header),
                     params=params, locations=locations, jumps=jumps)
