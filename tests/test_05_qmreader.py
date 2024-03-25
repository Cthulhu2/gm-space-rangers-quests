import logging
import os.path

import pytest

from srqmplayer.qmreader import parse
from srqmplayer.qmmodels import (
    ParamType, ParamCritType, ParameterShowingType, QM
)
from tests import TEST_RESOURCE_DIR

log = logging.getLogger()


# noinspection PyRedundantParentheses
@pytest.mark.parametrize(('filename'), ((f'qmreader-1.qm'),
                                        (f'qmreader-1.qmm')))
def test_reader(filename: str):
    with open(os.path.join(TEST_RESOURCE_DIR, filename), 'rb') as f:
        qm: QM = parse(f)
    _, ext = os.path.splitext(filename)
    log.info('Basic values')
    assert qm.hardness == 68
    assert qm.taskText == 'TaskText'
    assert qm.successText == 'SuccessText'

    assert qm.strings.Ranger == 'R'
    assert qm.strings.ToPlanet == 'TP'
    assert qm.strings.ToStar == 'TS'
    assert qm.strings.FromPlanet == 'FP'
    assert qm.strings.FromStar == 'FS'

    assert qm.defaultJumpCountLimit == 34

    log.info('Param definitions')
    log.info('param1')

    param = qm.params[0]
    assert param.active is True
    assert param.name == 'param1'
    assert param.type == ParamType.Обычный
    assert param.showWhenZero is True
    assert param.min == 0
    assert param.max == 1
    assert param.isMoney is False

    log.info('param2')
    param = qm.params[1]
    assert param.active is True
    assert param.name == 'param2success'
    assert param.type == ParamType.Успешный
    assert param.critType == ParamCritType.Минимум
    assert param.critValueString == 'def_param2_msg'
    if ext == '.qmm':
        assert param.img == 'p2img'
        assert param.track == 'p2track'
        assert param.sound == 'p2sound'
    else:
        assert param.img is None
        assert param.track is None
        assert param.sound is None

    log.info('param3')
    param = qm.params[2]
    assert param.active is True
    assert param.name == 'param3fail'
    assert param.type == ParamType.Провальный
    assert param.critType == ParamCritType.Максимум
    assert param.critValueString == 'p3_def_msg'
    if ext == '.qmm':
        assert param.img == 'p3img'
        assert param.track == 'p3track'
        assert param.sound == 'p3sound'
    else:
        assert param.img is None
        assert param.track is None
        assert param.sound is None

    log.info('param4')
    param = qm.params[3]
    assert param.active is True
    assert param.name == 'param4dead'
    assert param.type == ParamType.Смертельный

    log.info('param5')
    param = qm.params[4]
    assert param.active is True
    assert param.name == 'param5hidezero'
    assert param.showWhenZero is False

    log.info('param6startingval')
    param = qm.params[5]
    assert param.active is True
    assert param.name, 'param6startingval'
    assert param.min, 40
    assert param.max, 60
    assert param.starting, '[41]'

    log.info('param7showingranges')
    param = qm.params[6]
    assert param.active is True
    assert param.name, 'param7showingranges'

    # assert param.showingRangesCount, 3
    assert len(param.showingInfo) == 3

    assert param.showingInfo[0].from_ == 0
    assert param.showingInfo[0].to == 2
    assert param.showingInfo[0].str == 'range1 <>'

    assert param.showingInfo[1].from_ == 3
    assert param.showingInfo[1].to == 5
    assert param.showingInfo[1].str == 'range2 <>'

    assert param.showingInfo[2].from_ == 6
    assert param.showingInfo[2].to == 10
    assert param.showingInfo[2].str == 'range3 <>'

    log.info('param8money')
    param = qm.params[7]
    assert param.active is True
    assert param.name, 'param8money'
    assert param.isMoney is True

    log.info('Locations')
    log.info('Starting loc id=2')
    loc = next(filter(lambda l: l.id == 2, qm.locations), None)
    assert loc
    assert loc.texts[0] == 'loc2start'
    assert loc.isStarting is True
    assert loc.maxVisits == 0

    log.info('Text and sounds')
    loc = next(filter(lambda l: l.id == 1, qm.locations), None)
    assert loc, 'Location not found!'
    assert loc.isStarting is False
    if ext == '.qmm':
        assert len(loc.texts) == 3
        assert len(loc.media) == 3
    else:
        assert len(loc.texts) == 10
        assert len(loc.media) == 10

    for i in range(3):
        assert loc.texts[i] == f'loc1text{i + 1}'
        if ext == '.qmm':
            assert loc.media[i].img == f'loc1text{i + 1}img'
            assert loc.media[i].track == f'loc1text{i + 1}track'
            assert loc.media[i].sound == f'loc1text{i + 1}sound'
        else:
            assert loc.media[i].img is None
            assert loc.media[i].track is None
            assert loc.media[i].sound is None

    assert loc.isTextByFormula is False

    log.info('Text and sounds by formula')
    loc = next(filter(lambda l: l.id == 3, qm.locations), None)
    assert loc, 'Location not found!'
    assert loc.isTextByFormula is True
    assert loc.textSelectFormula, '[p1]+1'

    log.info('Empty loc')
    assert next(filter(lambda l: l.id == 5, qm.locations)).isEmpty

    log.info('Success loc')
    assert next(filter(lambda l: l.id == 6, qm.locations)).isSuccess
    log.info('Fail loc')
    assert next(filter(lambda l: l.id == 7, qm.locations)).isFaily
    log.info('Dead loc')
    assert next(filter(lambda l: l.id == 8, qm.locations)).isFailyDeadly
    log.info('Daypassed loc')
    assert next(filter(lambda l: l.id == 9, qm.locations)).dayPassed

    log.info('Visit limit loc id=10')
    assert next(filter(lambda l: l.id == 10,
                       qm.locations)).maxVisits == (78 if ext == '.qmm' else 0)

    log.info('Visit limit loc id=5')
    assert next(filter(lambda l: l.id == 5,
                       qm.locations)).maxVisits == (312 if ext == '.qmm' else 0)

    log.info('Location param change')
    loc = next(filter(lambda l: l.id == 4, qm.locations), None)
    assert loc, 'Location id=4 not found'
    log.info('param1 no change')
    param = loc.paramsChanges[0]
    assert param.change == 0
    assert param.isChangeFormula is False
    assert param.isChangePercentage is False
    assert param.isChangeValue is False
    assert param.showingType == ParameterShowingType.НеТрогать

    log.info('param2 changes')
    param = loc.paramsChanges[1]
    assert param.change == -1
    assert param.isChangeFormula is False
    assert param.isChangePercentage is False
    assert param.isChangeValue is False
    assert param.showingType == ParameterShowingType.Скрыть
    assert param.critText == 'l4_param2_msg'
    if ext == '.qmm':
        assert param.img == 'l4p2img'
        assert param.sound == 'l4p2sound'
        assert param.track == 'l4p2track'
    else:
        assert param.img is None
        assert param.track is None
        assert param.sound is None

    log.info('param3 changes')
    param = loc.paramsChanges[2]
    assert param.change == 44
    assert not param.isChangeFormula
    assert param.isChangePercentage
    assert not param.isChangeValue
    assert param.showingType == ParameterShowingType.Показать
    assert param.critText == 'l4_p3_msg'

    log.info('param6 changes')
    param = loc.paramsChanges[5]
    assert param.change == 53
    assert not param.isChangeFormula
    assert not param.isChangePercentage
    assert param.isChangeValue

    log.info('param7 changes')
    param = loc.paramsChanges[6]
    assert param.changingFormula == '[p3]-[p1]'
    assert param.isChangeFormula
    assert not param.isChangePercentage
    assert not param.isChangeValue

    log.info('Jumps')
    log.info('Jump id=2')
    jump = next(filter(lambda j: j.id == 2, qm.jumps))
    assert jump, 'Jump not found'
    assert jump.text == 'J2text'
    assert not jump.description
    assert jump.fromLocationId == 2
    assert jump.toLocationId == 1
    assert not jump.formulaToPass
    assert not jump.dayPassed
    assert not jump.alwaysShow
    assert jump.jumpingCountLimit == 0
    assert 0 <= abs(jump.priority - 1) < 0.000001, 'Jump prio'
    assert jump.showingOrder == 4

    log.info('Jump id=3')
    jump = next(filter(lambda j: j.id == 3, qm.jumps))
    assert jump, 'Jump not found'
    assert jump.text == 'J3text'
    assert jump.description == 'J3desciption'
    assert jump.fromLocationId == 7
    assert jump.toLocationId == 9
    assert jump.formulaToPass == '[p4]*[p2]'
    if ext == '.qmm':
        assert jump.img == 'j3_img'
        assert jump.track == 'j3_track'
        assert jump.sound == 'j3_sound'
    else:
        assert jump.img is None
        assert jump.track is None
        assert jump.sound is None

    assert jump.dayPassed
    assert not jump.alwaysShow
    assert jump.jumpingCountLimit == 34
    assert 0 <= abs(jump.priority - 1.5) < 0.000001, 'Jump prio'
    assert jump.showingOrder == 5

    log.info('Jump id=4')
    jump = next(filter(lambda j: j.id == 4, qm.jumps))
    assert jump, 'Jump not found'
    assert jump.text == 'alwaysShow'
    assert jump.alwaysShow
    assert jump.jumpingCountLimit == 78
    assert 0 <= abs(jump.priority - 0.2) < 0.000001, 'Jump prio'
    assert jump.showingOrder == 9

    log.info('Jump params requirements at jump5')
    jump = next(filter(lambda j: j.id == 5, qm.jumps))
    assert jump, 'Jump not found'
    log.info('Param 6 fullrange permit')
    param = jump.paramsConditions[5]
    assert param.mustFrom == qm.params[5].min
    assert param.mustTo == qm.params[5].max
    assert len(param.mustEqualValues) == 0
    assert len(param.mustModValues) == 0

    log.info('Param 9 min and max only')
    param = jump.paramsConditions[8]
    assert param.mustFrom == 77
    assert param.mustTo == 222
    assert len(param.mustEqualValues) == 0
    assert len(param.mustModValues) == 0

    log.info('Param 10 values list')
    param = jump.paramsConditions[9]
    assert param.mustEqualValues == [56, 58, 81]
    assert param.mustEqualValuesEqual

    log.info('Param 11 values list')
    param = jump.paramsConditions[10]
    assert param.mustEqualValues == [66, 69]
    assert not param.mustEqualValuesEqual

    log.info('Param 12 values list')
    param = jump.paramsConditions[11]
    assert param.mustModValues == [44]
    assert param.mustModValuesMod

    log.info('Param 13 values list')
    param = jump.paramsConditions[12]
    assert param.mustModValues == [45, 46]
    assert not param.mustModValuesMod

    log.info('Jump params change at jump6')

    jump = next(filter(lambda j: j.id == 6, qm.jumps))
    assert jump, 'Jump not found'
    log.info('Param 6')
    param = jump.paramsChanges[5]
    assert param.showingType == ParameterShowingType.НеТрогать
    assert param.change == 0
    assert not param.isChangeValue
    assert not param.isChangePercentage
    assert not param.isChangeFormula

    log.info('Param 9')
    param = jump.paramsChanges[8]
    assert param.showingType == ParameterShowingType.Скрыть
    assert param.change == -46
    assert not param.isChangeValue
    assert param.isChangePercentage
    assert not param.isChangeFormula

    log.info('Param 10')
    param = jump.paramsChanges[9]
    assert param.showingType == ParameterShowingType.Показать
    assert param.change == 48
    assert param.isChangeValue
    assert not param.isChangePercentage
    assert not param.isChangeFormula

    log.info('Param 11')
    param = jump.paramsChanges[10]
    assert param.showingType == ParameterShowingType.НеТрогать
    # assert param.change, 0
    assert not param.isChangeValue
    assert not param.isChangePercentage
    assert param.isChangeFormula
    assert param.changingFormula == '[p10]-[p4]+[p2]'

    log.info('Param 12')
    param = jump.paramsChanges[11]
    assert param.showingType == ParameterShowingType.НеТрогать
    assert param.change == 27
    assert not param.isChangeValue
    assert not param.isChangePercentage
    assert not param.isChangeFormula

    log.info('Param 3 crits')
    param = jump.paramsChanges[2]
    assert param.critText, 'j6_p3_fail_msg'
    if ext == '.qmm':
        assert param.img, 'j6p3img'
        assert param.track, 'j6p3track'
        assert param.sound, 'j6p3sound'
    else:
        assert param.img is None
        assert param.track is None
        assert param.sound is None
