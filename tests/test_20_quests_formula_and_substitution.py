import logging
from os import listdir
from os.path import join

from srqmplayer.formula import calculate, ParamValues
from srqmplayer.qmmodels import QM, ParamType
from srqmplayer.qmplayer import Lang, QMPlayer
from srqmplayer.qmplayer.defs import DEFAULT_DAYS_TO_PASS_QUEST
from srqmplayer.qmplayer.funcs import sr_date_to_str
from srqmplayer.qmplayer.playerSubstitute import PlayerSubstitute
from srqmplayer.qmreader import parse
from srqmplayer.randomFunc import rnd, create_determenistic_random
from srqmplayer.substitution import substitute
from tests import TEST_RESOURCE_DIR

log = logging.getLogger()
BORROWED_QUEST_DIR = join(TEST_RESOURCE_DIR, '../../borrowed/qm/')


def check(player_subs: PlayerSubstitute, quest: QM,
          param_values: ParamValues, str_: str, place: str = '',
          is_diamond: bool = False):
    try:
        substitute(
            str_,
            player_subs,
            param_values,
            quest.params,
            rnd,
            1 if is_diamond else None,
        )
    except Exception as err:
        raise Exception(f'String failed \'{str_}\' in {place}') from err


def check_formula(param_values: ParamValues, str_: str, place: str = ''):
    static_random_generated = [
        0.8098721706321894, 0.7650745137670785, 0.5122628148859116,
        0.7001314250579083,
        0.9777148783782501, 0.6484951526791192, 0.6277520602629139,
        0.6271209273581702,
        0.5929518455455183, 0.555114104030954, 0.8769248658117874,
        0.9012611135928128,
        0.9887903872842161, 0.9032020764410791, 0.09244706438405847,
        0.6841815116128189,
        0.26661520895002355, 0.95424331893931, 0.8900907263092355,
        0.9796112746203975,
    ]

    try:
        formulaResult = calculate(
            str_,
            create_determenistic_random(static_random_generated),
            param_values,
        )
    except Exception as err:
        raise Exception(f'String failed \'{str_}\' in {place}') from err


def get_game_task_text(task_text: str, player):
    p_subst = PlayerSubstitute.of(
        player,
        day=DEFAULT_DAYS_TO_PASS_QUEST,
        date=sr_date_to_str(DEFAULT_DAYS_TO_PASS_QUEST, player.lang),
        cur_date=sr_date_to_str(0, player.lang))

    return substitute(task_text, p_subst, ParamValues([]), [], rnd, None)


def test_checking_all_quests_for_formulas_and_params_substitution():
    for f in listdir(BORROWED_QUEST_DIR):
        if not f.endswith('.qm') and not f.endswith('.qmm'):
            continue
        fullname = join(BORROWED_QUEST_DIR, f)
        log.info(f'Checking quest {fullname}')
        player = PlayerSubstitute(
            Ranger='Ranger',
            Player='Player',
            FromPlanet='FromPlanet',
            FromStar='FromStar',
            ToPlanet='ToPlanet',
            ToStar='ToStar',
            Date='Date',
            Day='Day',
            Money='Money',
            CurDate='CurDate',
            lang=Lang.ru,
            allowBackButton=False
        )

        log.info('Loads quest and substitute variables')
        with open(fullname, 'rb') as data:
            quest = parse(data)

        def map_param(i, p):
            if p.active:
                # Just an example value
                return i * i
            else:
                # There are two quests which have formula
                # with disabled parameters
                # Let's return some random value
                # instead of undefined just to make this test pass
                return i * 3

        param_values = ParamValues(list(map(
            lambda tpl: map_param(tpl[0], tpl[1]),
            enumerate(quest.params))))

        log.info('Creates player and starts (to check init values)')
        QMPlayer(quest, Lang.ru).start()

        log.info('Starting/ending text')
        check(player, quest, param_values, quest.taskText, "start")
        check(player, quest, param_values, quest.successText, "success")

        log.info('Starting text as shown in main menu')
        get_game_task_text(quest.taskText, player)

        log.info('Locations texts and formulas')
        for loc in quest.locations:
            if ((f == 'Doomino.qm' and loc.id == 28)
                    or (f == 'Kiberrazum.qm' and loc.id == 134)):
                pass
                # Doomino: Какой-то там странный текст.
                # Эта локация пустая и все переходы в неё с описанием
                # Kiberrazum: просто локация без переходов в неё
                # Вообще-то это можно и автоматически фильтровать
            else:
                for x in loc.texts:
                    x and check(player, quest, param_values, x, f'Loc {loc.id}')

            for i, p in enumerate(loc.paramsChanges):
                if p.critText != quest.params[i].critValueString:
                    check(player, quest, param_values, p.critText,
                          f'Loc {loc.id} crit param {i}')

                if (quest.params[i].active
                        and p.isChangeFormula
                        and p.changingFormula):
                    check_formula(param_values, p.changingFormula,
                                  f'param {i} in loc={loc.id}')

            if loc.isTextByFormula and loc.textSelectFormula:
                check_formula(param_values, loc.textSelectFormula,
                              f'loc={loc.id} text select formula')

        log.info('Jumps texts and formulas')
        for jump in quest.jumps:
            if jump.text:
                check(player, quest, param_values, jump.text,
                      f'Jump {jump.id} text')

            if jump.description:
                check(player, quest, param_values, jump.description,
                      f'Jump {jump.id} decr')

            for i, p in enumerate(jump.paramsChanges):
                if p.critText != quest.params[i].critValueString:
                    check(player, quest, param_values, p.critText,
                          f'Jump {jump.id} crit param {i}')

                if (quest.params[i].active
                        and p.isChangeFormula
                        and p.changingFormula):
                    check_formula(param_values, p.changingFormula,
                                  f'param {i} in jump={jump.id}')
            if jump.formulaToPass:
                check_formula(param_values, jump.formulaToPass,
                              f'Jump id={jump.id} formula to pass')

        log.info('Params ranges')
        for i, p in enumerate(quest.params):
            for range_ in p.showingInfo:
                check(player, quest, param_values, range_.str,
                      f'Param {i} range', True)

        log.info('Params critText')
        for i, p in enumerate(quest.params):
            if p.type == ParamType.Обычный:
                continue
            if p.critValueString:
                check(player, quest, param_values, p.critValueString,
                      f'Param [p{i + 1}] critText', True)
            else:
                pass
                # raise Exception(f'Param {i} has no critValueString')
