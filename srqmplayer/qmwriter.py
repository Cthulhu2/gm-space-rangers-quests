import io
import struct
from typing import Optional

from srqmplayer.qmmodels import (
    LocationType, QMParam, ParameterChangeType, ParameterChange,
    ParameterShowingType, JumpParameterCondition,
    QM, HEADER_QM_2, HEADER_QM_3, HEADER_QM_4, HEADER_QMM_6,
    HEADER_QMM_7, HEADER_QMM_7_WITH_OLD_TGE_BEHAVIOUR,
)


class Writer:
    data: io.BytesIO

    def __init__(self, data: io.BytesIO):
        self.data = data

    def export(self):
        self.data.seek(0, 0)
        buf = self.data.read()
        self.data.seek(0, 2)
        return buf

    def int32(self, i: int):
        self.data.write(int.to_bytes(i, 4, 'little', signed=True))

    def write_string(self, str_: Optional[str]):
        if str_ is None:
            self.int32(0)
        else:
            self.int32(1)
            buf = str_.encode('utf-16-le')
            length = int(len(buf) / 2)
            self.int32(length)
            self.data.write(buf)

    def byte(self, b: int):
        self.data.write(int.to_bytes(b, 1, "little", signed=False))

    def float64(self, val: float):
        pack = struct.pack('<d', val)
        self.data.write(pack)


def write_param_change(w: Writer, param: ParameterChange, param_idx: int):
    w.int32(param_idx + 1)
    w.int32(param.change)
    w.byte(param.showingType)

    change_type = ParameterChangeType.Formula if param.isChangeFormula \
        else ParameterChangeType.Value if param.isChangeValue \
        else ParameterChangeType.Percentage if param.isChangePercentage \
        else ParameterChangeType.Summ
    w.byte(change_type)

    w.write_string(param.changingFormula)

    w.write_string(param.critText)
    w.write_string(param.img)
    w.write_string(param.sound)
    w.write_string(param.track)


def is_param_change_changed(param: ParameterChange) -> bool:
    return (param.change != 0
            or param.showingType != ParameterShowingType.НеТрогать
            or param.isChangeFormula
            or param.isChangeValue
            or param.isChangePercentage
            or param.changingFormula
            or param.critText
            or param.img
            or param.sound
            or param.track)


def is_jump_parameter_condition_changed(condition: JumpParameterCondition,
                                        param: QMParam) -> bool:
    return (condition.mustFrom != param.min
            or condition.mustTo != param.max
            or len(condition.mustEqualValues) > 0
            or condition.mustEqualValuesEqual
            or len(condition.mustModValues) > 0
            or condition.mustModValuesMod)


def write_qmm(quest: QM, data: io.BytesIO):
    w = Writer(data)
    if quest.header in (HEADER_QMM_7_WITH_OLD_TGE_BEHAVIOUR,
                        HEADER_QM_2, HEADER_QM_3, HEADER_QM_4):
        w.int32(HEADER_QMM_7_WITH_OLD_TGE_BEHAVIOUR)
    elif quest.header in (HEADER_QMM_7, HEADER_QMM_6):
        w.int32(HEADER_QMM_7)
    else:
        raise Exception(f'Unsupported header: 0x{quest.header:0x}')

    w.int32(1 if quest.majorVer is None else quest.majorVer)
    w.int32(0 if quest.minorVer is None else quest.minorVer)

    w.write_string(quest.changeLogStr)

    w.byte(quest.givingRace)
    w.byte(quest.whenDone)
    # noinspection PyTypeChecker
    w.byte(quest.planetRace.value)
    w.byte(quest.playerCareer)
    w.byte(quest.playerRace)
    w.int32(quest.reputationChange)

    w.int32(quest.screenSizeX)
    w.int32(quest.screenSizeY)
    w.int32(quest.widthSize)
    w.int32(quest.heightSize)
    w.int32(quest.defaultJumpCountLimit)
    w.int32(quest.hardness)

    # Params
    w.int32(len(quest.params))
    for param in quest.params:
        w.int32(param.min)
        w.int32(param.max)
        w.byte(param.type)

        w.byte(0)
        w.byte(0)
        w.byte(0)
        w.byte(1 if param.showWhenZero else 0)
        w.byte(param.critType)
        w.byte(1 if param.active else 0)
        w.int32(len(param.showingInfo))
        w.byte(1 if param.isMoney else 0)
        w.write_string(param.name)
        for showingRange in param.showingInfo:
            w.int32(showingRange.from_)
            w.int32(showingRange.to)
            w.write_string(showingRange.str)

        w.write_string(param.critValueString)
        w.write_string(param.img)
        w.write_string(param.sound)
        w.write_string(param.track)
        w.write_string(param.starting)

    w.write_string(quest.strings.ToStar)
    w.write_string(quest.strings.ToPlanet)
    w.write_string(quest.strings.Date)
    w.write_string(quest.strings.Money)
    w.write_string(quest.strings.FromPlanet)
    w.write_string(quest.strings.FromStar)
    w.write_string(quest.strings.Ranger)

    w.int32(len(quest.locations))
    w.int32(len(quest.jumps))

    w.write_string(quest.successText)

    w.write_string(quest.taskText)

    for loc in quest.locations:
        w.int32(1 if loc.dayPassed else 0)
        w.int32(loc.locX)
        w.int32(loc.locY)
        w.int32(loc.id)
        w.int32(loc.maxVisits)

        type_ = LocationType.Starting if loc.isStarting \
            else LocationType.Success if loc.isSuccess \
            else LocationType.Empty if loc.isEmpty \
            else LocationType.Deadly if loc.isFailyDeadly \
            else LocationType.Faily if loc.isFaily \
            else LocationType.Ordinary
        w.byte(type_)

        affected_params_change = [(i, param)
                                  for i, param in enumerate(loc.paramsChanges)
                                  if is_param_change_changed(param)]

        w.int32(len(affected_params_change))
        for i, param in affected_params_change:
            write_param_change(w, param, i)

        w.int32(len(loc.texts))
        for i in range(len(loc.texts)):
            w.write_string(loc.texts[i])
            media = loc.media[i]
            w.write_string(media.img if media else None)
            w.write_string(media.sound if media else None)
            w.write_string(media.track if media else None)

        w.byte(1 if loc.isTextByFormula else 0)
        w.write_string(loc.textSelectFormula)

    for jump in quest.jumps:
        w.float64(jump.priority)
        w.int32(1 if jump.dayPassed else 0)
        w.int32(jump.id)
        w.int32(jump.fromLocationId)
        w.int32(jump.toLocationId)
        w.byte(1 if jump.alwaysShow else 0)
        w.int32(jump.jumpingCountLimit)
        w.int32(jump.showingOrder)

        affected_jump_condition_params = [
            (i, param)
            for i, param in enumerate(jump.paramsConditions)
            if is_jump_parameter_condition_changed(param, quest.params[i])
        ]

        w.int32(len(affected_jump_condition_params))
        for i, cond in affected_jump_condition_params:
            w.int32(i + 1)
            w.int32(cond.mustFrom)
            w.int32(cond.mustTo)

            w.int32(len(cond.mustEqualValues))
            w.byte(1 if cond.mustEqualValuesEqual else 0)
            for val in cond.mustEqualValues:
                w.int32(val)

            w.int32(len(cond.mustModValues))
            w.byte(1 if cond.mustModValuesMod else 0)
            for val in cond.mustModValues:
                w.int32(val)

        affected_params_change = [(i, param)
                                  for i, param in enumerate(jump.paramsChanges)
                                  if is_param_change_changed(param)]
        w.int32(len(affected_params_change))
        for i, param in affected_params_change:
            write_param_change(w, param, i)

        w.write_string(jump.formulaToPass)
        w.write_string(jump.text)
        w.write_string(jump.description)
        w.write_string(jump.img)
        w.write_string(jump.sound)
        w.write_string(jump.track)

    return w.export()
