import logging
import re
from typing import List, Optional

from srqmplayer import RandomFunc
from srqmplayer.formula import ParamValues, calculate
from srqmplayer.qmmodels import QMParamShowInfo
from srqmplayer.qmplayer.playerSubstitute import PlayerSubstitute

clr = '<clr>'
clrEnd = '<clrEnd>'

PLAYER_KEYS_TO_REPLACE = [
    "Ranger",
    "Player",
    "FromPlanet",
    "FromStar",
    "ToPlanet",
    "ToStar",
    "Money",
    "Date",
    "Day",
    "CurDate",
]  # TODO: Maybe move from here

log = logging.getLogger()


def substitute(str_: str,
               player: PlayerSubstitute,
               param_values: ParamValues,
               param_show_infos: List[QMParamShowInfo],
               rnd: RandomFunc,
               diamond_idx: Optional[int]) -> str:
    """Replaces:

| <>           -> value of parameter with index = diamondIndex (if provided)
| {1+2}        -> parse formula, using random
| <Ranger>     -> player.Ranger and others
| [p22]        -> Value of parameter
| [d1]         -> Param 1 text with current value
| [d1:440 + 4] -> Param 1 text with value = 444 (see tests for supported cases)
|
| All replaced values have <clr>...<clrEnd> around them
"""
    # TODO: Use scanning method, go char by char.
    # Do not use .replace due to side-effect of special chars
    if diamond_idx is not None:
        str_ = str_.replace('<>', f'[p{diamond_idx + 1}]')

    search_pos = 0
    while True:
        d_idx = str_.find('[d', search_pos)

        if d_idx == -1:
            break

        scan_idx = d_idx + 2

        while True:
            current_char = str_[scan_idx]
            if current_char not in ('0', '1', '2', '3', '4', '5', '6', '7',
                                    '8', '9'):
                break
            scan_idx += 1

        param_idx_str = str_[d_idx + 2:scan_idx]
        if param_idx_str == '':
            log.warning(f'No param index found in \'{str_}\' at {d_idx}')
            search_pos = scan_idx
            continue

        p_idx = int(param_idx_str) - 1

        param_value = param_values[p_idx] if len(param_values) > p_idx else None

        if param_value is None:
            scan_idx += 1
            str_ = f'{str_[0:d_idx]}{clr}UNKNOWN_PARAM{clrEnd}{str_[scan_idx:]}'
            continue

        if str_[scan_idx] == ']':
            # Just keep param value as is
            scan_idx += 1
        elif str_[scan_idx] == ':':
            # Replace param value with formula
            scan_idx += 1
            formula_start_idx = scan_idx
            formula_end_idx = formula_start_idx
            while str_[scan_idx] == ' ':
                scan_idx += 1

            # And here goes the formula parsing
            # TODO: Use parse() method without throwing errors
            # So, parse() should read the expression
            # and return the index where it ends
            # Now we just using naive implementation
            # and counting square brackets
            square_brackets_count = 0
            while True:
                if str_[scan_idx] == '[':
                    square_brackets_count += 1
                elif str_[scan_idx] == ']':
                    if square_brackets_count == 0:
                        formula_end_idx = scan_idx
                        scan_idx += 1
                        break
                    else:
                        square_brackets_count -= 1

                scan_idx += 1
                if scan_idx > len(str_):
                    log.warning(f'No closing bracket found in \'{str_}\''
                                f' at {formula_start_idx}')
                    break
            formula_with_maybe_curly_brackets = \
                str_[formula_start_idx:formula_end_idx]

            formula = formula_with_maybe_curly_brackets
            inside_curly_brackets_match = \
                re.match(r'\s*\{(.*)}\s*', formula_with_maybe_curly_brackets)
            if inside_curly_brackets_match:
                formula = inside_curly_brackets_match[1]

            param_value = calculate(formula, rnd, param_values)
        else:
            log.warning(f'Unknown symbol in \'{str_}\' at {scan_idx}')
            break

        # TODO: This is very similar to getParamsState function,
        #       maybe better to refactor
        for showInfoRange in param_show_infos[p_idx].showingInfo:
            if showInfoRange.from_ <= param_value <= showInfoRange.to:
                param_str = substitute(showInfoRange.str,
                                       player,
                                       param_values,
                                       param_show_infos,
                                       rnd,
                                       diamond_idx)
                str_ = f'{str_[0:d_idx]}' \
                       f'{clr}{param_str}{clrEnd}' \
                       f'{str_[scan_idx:]}'
                break

        search_pos = scan_idx

    while True:
        m = re.search(r'\{[^\}]*\}', str_)
        if not m:
            break

        formula_with_brackets = m[0]
        result = calculate(
            formula_with_brackets[1:len(formula_with_brackets) - 1],
            rnd,
            param_values)
        str_ = str_.replace(formula_with_brackets, f'{clr}{result}{clrEnd}')

    for k in PLAYER_KEYS_TO_REPLACE:
        str_ = f'{clr}{getattr(player, k)}{clrEnd}'.join(str_.split(f'<{k}>'))

    for ii in range(len(param_values)):
        str_ = str_.replace(f'[p{ii + 1}]', f'{clr}{param_values[ii]}{clrEnd}')

    return str_
