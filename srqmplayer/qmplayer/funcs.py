import dataclasses
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from functools import reduce
from random import random
from typing import List, Optional, Dict, Tuple, cast

from dataclasses_json import dataclass_json

from srqmplayer import RandomFunc
from srqmplayer.alea import AleaState, Alea
from srqmplayer.formula import calculate, ParamValues
from srqmplayer.qmmodels import (
    QM, Location, ParamType, ParameterChange,
    ParameterShowingType, ParamCritType, HEADER_QM_2,
    HEADER_QM_3, HEADER_QM_4, HEADER_QMM_7_WITH_OLD_TGE_BEHAVIOUR, Jump
)
from srqmplayer.qmplayer import (
    DEFAULT_DAYS_TO_PASS_QUEST, JUMP_I_AGREE, JUMP_NEXT, JUMP_GO_BACK_TO_SHIP,
    int2base
)
from srqmplayer.qmplayer.player import (
    Lang, Player, DEFAULT_RUS_PLAYER, DEFAULT_ENG_PLAYER, PlayerSubstitute
)
from srqmplayer.substitution import substitute

TEXTS_ENG = {'iAgree': 'I agree',
             'next': 'Next',
             'goBackToShip': 'Go back to ship',
             'death': 'The great ranger\'s life was numbered',
             'image': 'Image',
             'track': 'Track',
             'inv': 'Inventory',
             'sound': 'Sound'}

TEXTS_RUS = {'iAgree': 'Я берусь за это задание',
             'next': 'Далее',
             'goBackToShip': 'Вернуться на корабль',
             'death': 'Жизнь великого рейнджера была сочтена',
             'image': 'Изображение',
             'track': 'Дорожка',
             'inv': 'Инвентарь',
             'sound': 'Звук'}

log = logging.getLogger()


class Quest(QM):
    pass


@dataclass
class GameLogStep:
    dateUnix: int
    jumpId: int


@dataclass_json
@dataclass(frozen=True)
class GameLog:
    aleaSeed: str
    performedJumps: List[GameLogStep]


class State(Enum):
    starting = 'starting'
    location = 'location'
    # Если переход с описанием и следующая локация не пустая
    jump = 'jump'
    # Если переход с описанием и следующая локация не пустая,
    # и параметры достигли критичного
    jumpandnextcrit = 'jumpandnextcrit'
    # Параметр стал критичным на локации, доступен только один переход далее
    critonlocation = 'critonlocation'
    # Параметр стал критичным на локации, показывается сообщение последнее
    critonlocationlastmessage = 'critonlocationlastmessage'
    # Параметр стал критичным на переходе без описания
    critonjump = 'critonjump'
    returnedending = 'returnedending'


@dataclass_json
@dataclass
class PossibleJump:
    id: int
    active: bool


@dataclass_json
@dataclass(frozen=True)
class GameState(GameLog):
    state: State
    critParamId: Optional[int]
    locationId: int
    lastJumpId: Optional[int]
    possibleJumps: List[PossibleJump]
    paramValues: ParamValues
    paramShow: List[bool]
    jumpedCount: Dict[int, int]
    locationVisitCount: Dict[int, int]
    daysPassed: int
    imageName: Optional[str]
    trackName: Optional[str]
    soundName: Optional[str]

    aleaState: AleaState


@dataclass
class PlayerChoice:
    text: str
    jumpId: int
    active: bool

    @staticmethod
    def next(texts: Dict[str, str]):
        return PlayerChoice(jumpId=JUMP_NEXT, text=texts['next'], active=True)

    @staticmethod
    def go_back_to_ship(texts: Dict[str, str]):
        return PlayerChoice(jumpId=JUMP_GO_BACK_TO_SHIP,
                            text=texts['goBackToShip'],
                            active=True)


class GameStateEnum(Enum):
    running = 'running'
    fail = 'fail'
    win = 'win'
    dead = 'dead'


@dataclass
class PlayerState:
    text: str
    gameState: GameStateEnum
    choices: List[PlayerChoice] = field(default_factory=list)
    paramsState: List[str] = field(default_factory=list)
    imageName: Optional[str] = None
    trackName: Optional[str] = None
    soundName: Optional[str] = None


def init_game(quest: Quest, seed: str) -> GameState:
    alea = Alea(seed)

    start_loc = next(filter(lambda x: x.isStarting, quest.locations))
    if not start_loc:
        raise Exception('No start location!')

    def calc_param(p):
        if not p.active:
            return 0

        if p.isMoney:
            give_money = 2000
            money = give_money if p.max > give_money else p.max
            starting = f'[{money}]'
            return calculate(starting, alea.rnd, ParamValues([]))

        return calculate(p.starting.replace("h", ".."), alea.rnd,
                         ParamValues([]))

    starting_params = ParamValues(list(map(calc_param, quest.params)))
    starting_showing = [True] * len(quest.params)

    state = GameState(state=State.starting,
                      locationId=start_loc.id,
                      lastJumpId=None,
                      critParamId=None,
                      possibleJumps=[],
                      paramValues=starting_params,
                      paramShow=starting_showing,
                      jumpedCount={},
                      locationVisitCount={},
                      daysPassed=0,
                      imageName=None,
                      trackName=None,
                      soundName=None,
                      aleaState=alea.export_state(),
                      aleaSeed=seed,
                      performedJumps=[])

    return state


TRACK_NAME_RESET_DEFAULT_MUSIC = 'Quest'


def sr_date_to_str(days_to_add: int,
                   lang: Lang,
                   initial_date: datetime = None):  # TODO: use it

    if not initial_date:
        initial_date = datetime.now()

    d = initial_date + timedelta(days=days_to_add)
    if lang == Lang.en:
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November',
                  'December']
    else:
        months = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня',
                  'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября',
                  'Декабря']
    return f'{d.day} {months[d.month]} {d.year + 1000}'


# This function is almost the same as substitute, but it takes quest and state
def replace(
        str_: str, quest: Quest, state: GameState, player: Player,
        diamond_idx: Optional[int],
        # Calling this random affects only visual representation of the game.
        # It is used in few quests for example to make some random number
        # on location description.
        rnd: RandomFunc):
    return substitute(
        str_=str_,
        player=PlayerSubstitute.of(
            player,
            day=f'{DEFAULT_DAYS_TO_PASS_QUEST - state.daysPassed}',
            date=sr_date_to_str(DEFAULT_DAYS_TO_PASS_QUEST, player.lang),
            cur_date=sr_date_to_str(state.daysPassed, player.lang)),
        param_values=ParamValues(state.paramValues),
        param_show_infos=quest.params,
        rnd=rnd,
        diamond_idx=diamond_idx)


def get_params_state(quest: Quest, state: GameState, player: Player,
                     rnd: RandomFunc) -> List[str]:
    params_state: List[str] = []
    for i in range(quest.paramsCount):
        if state.paramShow[i] and quest.params[i].active:
            val = state.paramValues[i]
            param = quest.params[i]
            if val != 0 or param.showWhenZero:
                for part in param.showingInfo:
                    if part.from_ <= val <= part.to:
                        str_ = replace(part.str, quest, state, player, i, rnd)
                        params_state.append(str_)
                        break
    return params_state


def replace_special_track_name(track_name: Optional[str]):
    if track_name == TRACK_NAME_RESET_DEFAULT_MUSIC:
        return None
    return track_name


def calc_loc_showing_text_id(loc: Location,
                             state: GameState,
                             rnd: RandomFunc,
                             debug: bool) -> int:
    texts = [(i, txt) for i, txt in enumerate(loc.texts) if txt]

    if loc.isTextByFormula:
        if loc.textSelectFormula:
            id_ = calculate(loc.textSelectFormula, rnd,
                            state.paramValues) - 1
            if len(loc.texts) > id_ and loc.texts[id_]:
                return id_
            else:
                if debug:
                    log.warning(f'Location id={loc.id} formula result'
                                f' textId={id_}, but no text')
                # Tge 4 and 5 shows different here.
                # We will show location text 0
                return 0
        else:
            if debug:
                log.warning(f'Location id={loc.id} text by formula is set,'
                            f' but no formula')
            text_num = rnd(len(texts))
            return texts[text_num][0] if texts else 0
    else:
        text_num = state.locationVisitCount[loc.id] % len(texts) if texts else 0
        return texts[text_num][0] if texts else 0


def get_ui_state(quest: Quest, state: GameState, player: Player,
                 debug=False) -> PlayerState:
    alea = Alea(AleaState(state.aleaState))
    rnd = alea.rnd

    texts = TEXTS_RUS if player.lang == Lang.ru else TEXTS_ENG

    if state.state == State.starting:
        return PlayerState(
            text=replace(quest.taskText, quest, state, player, None, rnd),
            choices=[PlayerChoice(jumpId=JUMP_I_AGREE,
                                  text=texts['iAgree'],
                                  active=True)],
            gameState=GameStateEnum.running)
    elif state.state == State.jump:
        jump = quest.get_jump(state.lastJumpId)
        return PlayerState(
            text=replace(jump.description, quest, state, player, None,
                         alea.rnd),
            paramsState=get_params_state(quest, state, player, rnd),
            choices=[PlayerChoice.next(texts)],
            gameState=GameStateEnum.running,
            imageName=state.imageName,
            trackName=replace_special_track_name(state.trackName),
            soundName=state.soundName
        )
    elif state.state in (State.location, State.critonlocation):
        loc = quest.get_loc(state.locationId)
        loc_text_id = calc_loc_showing_text_id(loc, state, rnd, debug)
        loc_own_text = (loc.texts[loc_text_id] or '') if loc.texts else ''

        last_jump = quest.find_jump(state.lastJumpId)
        if loc.isEmpty and last_jump and last_jump.description:
            text = last_jump.description
        else:
            text = loc_own_text

        if state.state == State.location:
            if loc.isFaily or loc.isFailyDeadly:
                choices = []
            elif loc.isSuccess:
                choices = [PlayerChoice.go_back_to_ship(texts)]
            else:
                def map_possible_jumps(p_jump):
                    jmp = quest.get_jump(p_jump.id)
                    return PlayerChoice(
                        text=replace(jmp.text, quest, state, player, None,
                                     alea.rnd) or texts['next'],
                        jumpId=p_jump.id,
                        active=p_jump.active)

                choices = list(map(map_possible_jumps, state.possibleJumps))
        else:  # critonlocation
            choices = [PlayerChoice.next(texts)]
        return PlayerState(
            text=replace(text, quest, state, player, None, alea.rnd),
            paramsState=get_params_state(quest, state, player, rnd),
            choices=choices,
            gameState=GameStateEnum.dead if loc.isFailyDeadly
            else GameStateEnum.fail if loc.isFaily
            else GameStateEnum.running,
            imageName=state.imageName,
            trackName=replace_special_track_name(state.trackName),
            soundName=state.soundName)
    elif state.state == State.critonjump:
        crit_id = state.critParamId
        jump = quest.find_jump(state.lastJumpId)
        if crit_id is None or not jump:
            raise Exception(f'Internal error: crit={crit_id}'
                            f' lastJump={state.lastJumpId}')
        param = quest.params[crit_id]
        if param.type == ParamType.Успешный:
            choices = [PlayerChoice.go_back_to_ship(texts)]
        else:
            choices = []
        return PlayerState(
            text=replace(jump.paramsChanges[crit_id].critText
                         or quest.params[crit_id].critValueString,
                         quest, state, player, None, alea.rnd),
            paramsState=get_params_state(quest, state, player, rnd),
            choices=choices,
            gameState=GameStateEnum.running if param.type == ParamType.Успешный
            else GameStateEnum.fail if param.type == ParamType.Провальный
            else GameStateEnum.dead,
            imageName=state.imageName,
            trackName=replace_special_track_name(state.trackName),
            soundName=state.soundName)
    elif state.state == State.jumpandnextcrit:
        crit_id = state.critParamId
        jump = quest.find_jump(state.lastJumpId)
        if crit_id is None or not jump:
            raise Exception(f'Internal error: crit={crit_id}'
                            f' lastJump={state.lastJumpId}')
        # const param = quest.params[critId];
        return PlayerState(
            text=replace(jump.description, quest, state, player, None,
                         alea.rnd),
            paramsState=get_params_state(quest, state, player, rnd),
            choices=[PlayerChoice.next(texts)],
            gameState=GameStateEnum.running,
            imageName=state.imageName,
            trackName=replace_special_track_name(state.trackName),
            soundName=state.soundName)
    elif state.state == State.critonlocationlastmessage:
        crit_id = state.critParamId
        if crit_id is None:
            raise Exception('Internal error: no critId')
        loc = quest.get_loc(state.locationId)
        param = quest.params[crit_id]
        if param.type == ParamType.Успешный:
            choices = [PlayerChoice.go_back_to_ship(texts)]
        else:
            choices = []
        return PlayerState(
            text=replace(loc.paramsChanges[crit_id].critText
                         or quest.params[crit_id].critValueString,
                         quest, state, player, None, alea.rnd),
            paramsState=get_params_state(quest, state, player, rnd),
            choices=choices,
            gameState=GameStateEnum.running if param.type == ParamType.Успешный
            else GameStateEnum.fail if param.type == ParamType.Провальный
            else GameStateEnum.dead,
            imageName=state.imageName,
            trackName=replace_special_track_name(state.trackName),
            soundName=state.soundName)
    elif state.state == State.returnedending:
        return PlayerState(
            text=replace(quest.successText, quest, state, player, None,
                         alea.rnd),
            gameState=GameStateEnum.win)
    else:
        raise Exception(f'Unexpected state {state.state}')


def calc_params_update(
        quest: Quest,
        state_orig: GameState,
        rnd: RandomFunc,
        params_changes: List[ParameterChange]
) -> Tuple[GameState, List[int]]:
    crit_params_triggered: List[int] = []
    state = dataclasses.replace(state_orig)
    old_values = state.paramValues[0:quest.paramsCount]
    new_values = state.paramValues[0:quest.paramsCount]

    param_show = list(state.paramShow)
    for i in range(quest.paramsCount):
        change = params_changes[i]
        if change.showingType == ParameterShowingType.Показать:
            param_show[i] = True
        elif change.showingType == ParameterShowingType.Скрыть:
            param_show[i] = False

        if change.isChangeValue:
            new_values[i] = change.change
        elif change.isChangePercentage:
            new_values[i] = round((old_values[i] * (100 + change.change)) / 100)
        elif change.isChangeFormula:
            if change.changingFormula:
                new_values[i] = calculate(change.changingFormula, rnd,
                                          old_values)
        else:
            new_values[i] = old_values[i] + change.change

        param = quest.params[i]
        if new_values[i] > param.max:
            new_values[i] = param.max
        if new_values[i] < param.min:
            new_values[i] = param.min

        if new_values[i] != old_values[i] and param.type != ParamType.Обычный:
            if ((param.critType == ParamCritType.Максимум
                 and new_values[i] == param.max)
                    or (param.critType == ParamCritType.Минимум
                        and new_values[i] == param.min)):
                crit_params_triggered.append(i)
    state = dataclasses.replace(state,
                                paramShow=param_show,
                                paramValues=new_values)
    return state, crit_params_triggered


def perform_jump(jump_id: int,
                 quest: Quest,
                 state_orig: GameState,
                 date_unix=None,
                 debug: bool = True) -> GameState:
    if date_unix is None:
        date_unix = datetime.now().timestamp()
    alea = Alea(AleaState(state_orig.aleaState))
    rnd = alea.rnd
    performed_jumps = [*state_orig.performedJumps,
                       GameLogStep(dateUnix=date_unix, jumpId=jump_id)]
    state = dataclasses.replace(state_orig,
                                performedJumps=performed_jumps,
                                # Clear sound name before jump
                                soundName=None)
    state = perform_jump_internal(jump_id, quest, state, rnd, debug)
    return dataclasses.replace(state, aleaState=alea.export_state())


def perform_jump_internal(jump_id: int,
                          quest: Quest,
                          state_orig: GameState,
                          rnd: RandomFunc,
                          debug: bool) -> GameState:
    if jump_id == JUMP_GO_BACK_TO_SHIP:
        return dataclasses.replace(state_orig, state=State.returnedending)

    state = state_orig

    # /*
    #  // Before for unknown reasons it used media from last jump
    #  // TODO: Test how original game behaves with media
    #
    #  const lastJumpMedia = quest.jumps.find((x) => x.id === state.lastJumpId);
    #  if (lastJumpMedia && lastJumpMedia.img) {
    #    state = {
    #      ...state,
    #      imageName: lastJumpMedia.img,
    #    };
    #  }
    # */

    jump = quest.find_jump(jump_id)
    state = dataclasses.replace(
        state,
        imageName=jump.img if jump and jump.img else state.imageName,
        trackName=replace_special_track_name(
            jump.track if jump and jump.track else state.trackName),
        soundName=jump.sound if jump and jump.sound else state.soundName)

    if state.state == State.starting:
        state = dataclasses.replace(state, state=State.location)
        state = calc_loc(quest, state, rnd, debug)
    elif state.state == State.jump:
        jump = quest.get_jump(state.lastJumpId)
        state = dataclasses.replace(state,
                                    locationId=jump.toLocationId,
                                    state=State.location)
        state = calc_loc(quest, state, rnd, debug)
    elif state.state == State.location:
        if not next(filter(lambda x: x.id == jump_id,
                           state.possibleJumps), None):
            raise Exception(
                f'Jump {jump_id} is not in list in that location.'
                f' Possible jumps={state.possibleJumps}')
        jump = quest.get_jump(jump_id)
        state = dataclasses.replace(state, lastJumpId=jump_id)
        if jump.dayPassed:
            state = dataclasses.replace(state, daysPassed=state.daysPassed + 1)

        state = dataclasses.replace(
            state,
            jumpedCount={
                **state.jumpedCount,
                jump_id: (state.jumpedCount[jump_id] or 0
                          if jump_id in state.jumpedCount else 0) + 1
            },
        )

        state, crit_params_triggered = \
            calc_params_update(quest, state, rnd, jump.paramsChanges)

        next_loc = quest.get_loc(jump.toLocationId)

        if not jump.description:
            if crit_params_triggered:
                crit_param_id = crit_params_triggered[0]
                state = dataclasses.replace(state,
                                            state=State.critonjump,
                                            critParamId=crit_param_id)
                state = dataclasses.replace(
                    state,
                    imageName=(jump.paramsChanges[crit_param_id].img
                               or quest.params[crit_param_id].img
                               or state.imageName),
                    trackName=replace_special_track_name(
                        jump.paramsChanges[crit_param_id].track
                        or quest.params[crit_param_id].track
                        or state.trackName),
                    soundName=(jump.paramsChanges[crit_param_id].sound
                               or quest.params[crit_param_id].sound
                               or state.soundName))
            else:
                state = dataclasses.replace(state,
                                            locationId=next_loc.id,
                                            state=State.location)
                state = calc_loc(quest, state, rnd, debug)
        else:
            if crit_params_triggered:
                state = dataclasses.replace(
                    state,
                    state=State.jumpandnextcrit,
                    critParamId=crit_params_triggered[0])
            elif next_loc.isEmpty:
                state = dataclasses.replace(state,
                                            locationId=next_loc.id,
                                            state=State.location)
                state = calc_loc(quest, state, rnd, debug)
            else:
                state = dataclasses.replace(state, state=State.jump)
    elif state.state == State.jumpandnextcrit:
        state = dataclasses.replace(state, state=State.critonjump)
        jump = quest.find_jump(state.lastJumpId)
        img = ''
        track = ''
        sound = ''
        if state.critParamId is not None:
            if jump and jump.paramsChanges[state.critParamId].img:
                img = jump.paramsChanges[state.critParamId].img
            img = img or quest.params[state.critParamId].img

            if jump and jump.paramsChanges[state.critParamId].track:
                track = jump.paramsChanges[state.critParamId].track
            track = track or quest.params[state.critParamId].track

            if jump and jump.paramsChanges[state.critParamId].sound:
                sound = jump.paramsChanges[state.critParamId].sound
            sound = sound or quest.params[state.critParamId].sound
        img = img or state.imageName
        track = track or state.trackName
        sound = sound or state.soundName

        state = dataclasses.replace(state,
                                    imageName=img,
                                    trackName=replace_special_track_name(track),
                                    soundName=sound)
    elif state.state == State.critonlocation:
        state = dataclasses.replace(state,
                                    state=State.critonlocationlastmessage)
    else:
        raise Exception(f'Unknown state {state.state} in performJump')

    return state


@dataclass
class JumpActive(Jump):
    active: bool

    @staticmethod
    def of(j: Jump, active: bool):
        return JumpActive(
            id=j.id, text=j.text, description=j.description,
            paramsChanges=j.paramsChanges, paramsConditions=j.paramsConditions,
            fromLocationId=j.fromLocationId, toLocationId=j.toLocationId,
            priority=j.priority, dayPassed=j.dayPassed, alwaysShow=j.alwaysShow,
            jumpingCountLimit=j.jumpingCountLimit, showingOrder=j.showingOrder,
            formulaToPass=j.formulaToPass,
            img=j.img, sound=j.sound, track=j.track,
            active=active)


def calc_loc(quest: Quest,
             state_orig: GameState,
             rnd: RandomFunc,
             debug: bool) -> GameState:
    if state_orig.state != State.location:
        raise Exception(f'Internal error: expecting "location" state')

    state = state_orig
    state = dataclasses.replace(
        state,
        locationVisitCount={
            **state.locationVisitCount,
            state.locationId:
                state.locationVisitCount[state.locationId] + 1
                if state.locationId in state.locationVisitCount
                else 0  # TODO: change to 1
        },
    )

    loc = quest.get_loc(state.locationId)
    loc_img_id = calc_loc_showing_text_id(loc, state, rnd, debug)
    loc_media = loc.media[loc_img_id] if loc.media else None
    state = dataclasses.replace(
        state,
        imageName=loc_media.img
        if loc_media and loc_media.img else state.imageName,
        trackName=replace_special_track_name(
            loc_media.track
            if loc_media and loc_media.track else state.trackName),
        soundName=loc_media.sound
        if loc_media and loc_media.sound else state.soundName
    )

    if loc.dayPassed:
        state = dataclasses.replace(state, daysPassed=state.daysPassed + 1)

    state, crit_params_triggered = \
        calc_params_update(quest, state, rnd, loc.paramsChanges)

    old_tge_behaviour = quest.header in (HEADER_QM_2, HEADER_QM_3, HEADER_QM_4,
                                         HEADER_QMM_7_WITH_OLD_TGE_BEHAVIOUR)

    def filter_jumps(jump: Jump) -> bool:
        # Сразу выкинуть переходы в локации с превышенным лимитом
        to_loc = quest.find_loc(jump.toLocationId)
        if (to_loc and to_loc.maxVisits
                and jump.toLocationId in state.locationVisitCount
                and state.locationVisitCount[jump.toLocationId] + 1
                >= to_loc.maxVisits):
            return False

        if old_tge_behaviour:
            # Это какая-то особенность TGE - не учитывать переходы,
            # которые ведут в локацию, где были переходы,
            # а проходимость закончилась.
            # Это вообще дикость какая-то, потому как там вполне может быть
            # критичный параметр завершить квест
            jumps_from_dest = [x for x in quest.jumps
                               if x.fromLocationId == jump.toLocationId]
            if not jumps_from_dest:
                # Но если там вообще переходов не было, то всё ок
                return True

            def limit_exceeded(j: Jump):
                return (j.jumpingCountLimit
                        and j.id in state.jumpedCount
                        and state.jumpedCount[j.id] >= j.jumpingCountLimit)

            all_jumps_used = len(list(filter(limit_exceeded, jumps_from_dest)))
            return all_jumps_used != len(jumps_from_dest)
        else:
            return True

    all_jumps_from_this_loc: List[Jump] = [
        x for x in quest.jumps
        if x.fromLocationId == state.locationId and filter_jumps(x)]

    def is_jump_active(jump: Jump):
        for i in range(quest.paramsCount):
            if quest.params[i].active:
                p_value = state.paramValues[i]
                p_condition = jump.paramsConditions[i]
                if (p_value > p_condition.mustTo
                        or p_value < p_condition.mustFrom):
                    return False

                if p_condition.mustEqualValues:
                    any_equal = list(filter(lambda x: x == p_value,
                                            p_condition.mustEqualValues))
                    if p_condition.mustEqualValuesEqual and not any_equal:
                        return False
                    if not p_condition.mustEqualValuesEqual and any_equal:
                        return False

                if p_condition.mustModValues:
                    any_mod = list(filter(lambda x: x != 0 and p_value % x == 0,
                                          p_condition.mustModValues))
                    if p_condition.mustModValuesMod and not any_mod:
                        return False

                    if not p_condition.mustModValuesMod and any_mod:
                        return False
        if jump.formulaToPass:
            if calculate(jump.formulaToPass, rnd, state.paramValues) == 0:
                return False

        if (jump.jumpingCountLimit
                and jump.id in state.jumpedCount
                and state.jumpedCount[jump.id] >= jump.jumpingCountLimit):
            return False

        return True

    # Если есть такие же тексты - то спорный по весам
    # Если текст один - то по вероятности

    # Own sorting realization to keep sorting "unstable" random,
    # but with same random between browsers */
    all_jumps_from_this_loc_sorted: List[Jump] = \
        sort_jumps(all_jumps_from_this_loc, rnd)

    #
    # console.info('-------------');
    # console.info('all', all_jumps_from_this_loc
    #   .map(x => `id=${x.id} prio=${x.showingOrder}`).join(', '));
    # console.info('sorted', all_jumps_from_this_loc_sorted
    #   .map(x => `id=${x.id} prio=${x.showingOrder}`).join(', '));
    #
    all_possible_jumps: List[JumpActive] = [
        JumpActive.of(x, active=is_jump_active(x))
        for x in all_jumps_from_this_loc_sorted]

    possible_jumps_with_same_text_grouped: List[JumpActive] = []

    seen_texts: Dict[str, bool] = {}

    for j in all_possible_jumps:
        if j.text in seen_texts and seen_texts[j.text]:
            continue
        seen_texts[j.text] = True
        jumps_with_same_text = [x for x in all_possible_jumps
                                if x.text == j.text]
        if len(jumps_with_same_text) == 1:
            if j.priority < 1 and j.active:
                accuracy = 1000
                j.active = rnd(accuracy) < j.priority * accuracy
                # log.info(f'Jump {j.jump.text} is now {j.active} by random')

            if j.active or j.alwaysShow:
                possible_jumps_with_same_text_grouped.append(j)
        else:
            jumps_active_with_same_text = [x for x in jumps_with_same_text
                                           if x.active]
            if jumps_active_with_same_text:
                max_prio = reduce(
                    lambda max_, jump:
                    jump.priority if jump.priority > max_ else max_,
                    jumps_active_with_same_text,
                    0)

                jumps_with_not_so_low_prio = [
                    x for x in jumps_active_with_same_text
                    if x.priority * 100 >= max_prio]
                prio_sum = sum(map(lambda x: x.priority,
                                   jumps_with_not_so_low_prio))

                accuracy = 1000000
                rnd_ = (rnd(accuracy) / accuracy) * prio_sum
                for jj in jumps_with_not_so_low_prio:
                    if (jj.priority >= rnd_
                            or jj == jumps_with_not_so_low_prio[:-1]):
                        possible_jumps_with_same_text_grouped.append(jj)
                        break
                    else:
                        rnd_ = rnd_ - jj.priority
            else:
                al_least_one_with_always_show = next(filter(
                    lambda x: x.alwaysShow, jumps_with_same_text), None)
                if al_least_one_with_always_show:
                    jumps_with_same_text.remove(al_least_one_with_always_show)
                    possible_jumps_with_same_text_grouped.append(
                        al_least_one_with_always_show)

    #   /*
    #     const newActiveJumpsWithoutEmpty =
    #       newJumps.filter(x => x.active && x.jump.text);
    #     const new_active_jumps_only_empty =
    #       newJumps.filter(x => x.active && !x.jump.text);
    #     const new_active_jumps_only_one_empty =
    #       new_active_jumps_only_empty.length > 0
    #       ? [new_active_jumps_only_empty[0]] : [];
    #
    #     this.state.possibleJumps = (newActiveJumpsWithoutEmpty.length > 0 ?
    #         newJumps.filter(x => x.jump.text) :
    #         new_active_jumps_only_one_empty)
    #         .map(x => {
    #             return {
    #                 active: x.active,
    #                 id: x.jump.id
    #             }
    #         })
    #         */
    new_jumps_w_text = [x for x in possible_jumps_with_same_text_grouped
                        if x.text]
    new_active_jumps_empty = [x for x in possible_jumps_with_same_text_grouped
                              if x.active and not x.text]
    new_active_jumps_empty_single = [new_active_jumps_empty[0]] \
        if new_active_jumps_empty else []

    state_possible_jumps = [PossibleJump(id=x.id, active=x.active)
                            for x in new_jumps_w_text
                            or new_active_jumps_empty_single]

    state = dataclasses.replace(state, possibleJumps=state_possible_jumps)

    for critParam in crit_params_triggered:
        got_faily_crit_with_choices = \
            (quest.params[critParam].type == ParamType.Провальный
             or quest.params[critParam].type == ParamType.Смертельный) \
            and any(filter(lambda x: x.active, state.possibleJumps))

        if old_tge_behaviour and got_faily_crit_with_choices:
            # Do nothing because some jumps allows this
            pass
        else:
            last_jump = quest.find_jump(state.lastJumpId)
            if loc.isEmpty:
                if state.lastJumpId and last_jump and last_jump.description:
                    state_ = State.critonlocation
                else:
                    state_ = State.critonlocationlastmessage
            else:
                state_ = State.critonlocation
            state = dataclasses.replace(state, state=state_,
                                        critParamId=critParam)
            state = dataclasses.replace(
                state,
                imageName=(loc.paramsChanges[critParam].img
                           or quest.params[critParam].img
                           or state.imageName),
                trackName=replace_special_track_name(
                    loc.paramsChanges[critParam].track
                    or quest.params[critParam].track
                    or state.trackName),
                soundName=(loc.paramsChanges[critParam].sound
                           or quest.params[critParam].sound
                           or state.soundName))

    # calculateLocation is always called when state.state === "location",
    # but state.state can change

    # А это дикий костыль для пустых локаций и переходов
    if state.state == State.location and len(state.possibleJumps) == 1:
        lonely_current_jump_in_possible = state.possibleJumps[0]
        lonely_current_jump = quest.get_jump(lonely_current_jump_in_possible.id)
        last_jump = quest.find_jump(state.lastJumpId)

        loc_text_id = calc_loc_showing_text_id(loc, state, rnd, debug)
        loc_own_text = (loc.texts[loc_text_id] or '') if loc.texts else ''

        # log.info(
        #    f'\nold_tge_behaviour={old_tge_behaviour} loc_own_text={loc_own_text} '
        #    f'isEmpty={loc.isEmpty} id=${loc.id} last_jump={bool(last_jump)} '
        #    f'lastJumpDesc='
        #    f'{last_jump.description if last_jump else "<nojump>"}'
        # )
        need_auto_jump = (
                lonely_current_jump_in_possible.active
                and not lonely_current_jump.text
                and ((not last_jump.description if last_jump else True)
                     if loc.isEmpty else not loc_own_text))

        if need_auto_jump:
            if debug:
                log.info(f'Performing auto-jump from loc={state.locationId}'
                         f' via jump={lonely_current_jump.id}')
            state = perform_jump_internal(lonely_current_jump.id, quest, state,
                                          rnd, debug)
    elif state.state == State.critonlocation:
        # Little bit copy-paste from branch above
        last_jump = quest.find_jump(state.lastJumpId)
        loc_text_id = calc_loc_showing_text_id(loc, state, rnd, debug)
        loc_own_text = loc.texts[loc_text_id] or ''
        if loc.isEmpty:
            if last_jump:
                loc_do_not_have_text = not last_jump.description
            else:
                loc_do_not_have_text = True
        else:
            loc_do_not_have_text = not loc_own_text
        if loc_do_not_have_text:
            state = dataclasses.replace(state,
                                        state=State.critonlocationlastmessage)
    return state


# /*
# export function validateState(
#     quest: Quest,
#     stateOriginal: GameState,
#     images: PQImages = []
# ) {
#     try {
#         let state = initGame(quest, stateOriginal.aleaSeed);
#         for (const performedJump of stateOriginal.performedJumps) {
#             state = performJump(
#                 performedJump.jumpId,
#                 quest,
#                 state,
#                 images,
#                 performedJump.dateUnix
#             );
#         }
#         assert.deepStrictEqual(stateOriginal, state);
#         return true;
#     } catch (e) {
#         console.info(e);
#         return false;
#     }
# }
# */


def sort_jumps(inp: List[Jump], rnd: RandomFunc) -> List[Jump]:
    output: List[Jump] = list(inp)
    for i in range(len(output)):
        min_showing_order: Optional[int] = None
        min_idxes: List[int] = []
        for ii in range(i, len(output)):
            cur_element = output[ii]
            if min_showing_order is None \
                    or cur_element.showingOrder < min_showing_order:
                min_showing_order = cur_element.showingOrder
                min_idxes = [ii]
            elif cur_element.showingOrder == min_showing_order:
                min_idxes.append(ii)

        min_idx = min_idxes[0] if (len(min_idxes) == 1) \
            else min_idxes[rnd(len(min_idxes))]
        # log.info(f'i={i} minimumIndex={min_idx} min_idxes={min_idxes}')
        swap = output[i]
        output[i] = output[min_idx]
        output[min_idx] = swap

    return output


class QMPlayer:
    quest: QM
    player: Player
    state: GameState
    playerState: PlayerState

    def __init__(self, quest, lang: Lang, ranger: str = None):
        self.quest = quest
        self.player = DEFAULT_RUS_PLAYER if lang == Lang.ru \
            else DEFAULT_ENG_PLAYER
        if ranger:
            self.player = dataclasses.replace(self.player,
                                              Ranger=ranger, Player=ranger)
        self.start()

    def start(self):
        self.state = init_game(cast(Quest, self.quest),
                               int2base(random() * 10_000_000_000, 36))
        self.playerState = get_ui_state(
            cast(Quest, self.quest), self.state, self.player)

    def is_available_jump(self, jump_id: int):
        return any(filter(lambda x: x.jumpId == jump_id and x.active,
                          self.get_state().choices))

    def get_state(self) -> PlayerState:
        return self.playerState

    def perform_jump(self, jump_id: int):
        if not self.is_available_jump(jump_id):
            raise Exception(f'Not available jumpId={jump_id}')
        self.state = perform_jump(jump_id, cast(Quest, self.quest), self.state)
        self.playerState = get_ui_state(
            cast(Quest, self.quest), self.state, self.player)

    def get_saving(self):
        return self.state

    def load_saving(self, state: GameState):
        self.state = state
        self.playerState = get_ui_state(
            cast(Quest, self.quest), self.state, self.player)
