import logging

from srqmplayer.formula.calculator import MAX_NUMBER
from srqmplayer.formula import calculate, ParamValues
from srqmplayer.randomFunc import rnd

log = logging.getLogger()


def test_formula_parser():
    log.info('Formula parser test')
    test_equations = {
        "2 + 2 * 2": 6,
        "2 +  2 * 2 +2+2": 10,
        "2+(2 *2 +3   )+4": 13,
        "5 + [3..3]*2": 11,
        "10 / 3": 3,
        "-10 / 3": -3,
        "10 / 3 * 3": 10,
        "10 / 2": 5,
        "10 / (-3)": -3,
        "10 / (-4)": -2,
        "-10 / (-4)": 3,
        "10 / 0": MAX_NUMBER,
        "-10 / 0": -MAX_NUMBER,
        "11 / 4": 3,
        "-11 / 4": -3,

        "10 div 3": 3,
        "10 div (-3)": -3,
        "-10 div (-3)": 3,
        "10 div 0": MAX_NUMBER,
        "-10 div 0": -MAX_NUMBER,
        "10 div 3 * 3": 9,
        "11 div 4": 2,
        "-11 div 4": -2,

        "10 mod 3": 1,
        "10 mod (-3)": 1,
        "-10 mod (-3)": -1,
        "10 mod 0": MAX_NUMBER,
        "-10 mod 0": -MAX_NUMBER,

        "2*3": 6,
        " -3 * (- 3)": 9,
        "4*(-3)": -12,

        "4 * -  3": -12,

        "-4 * -3": 12,
        "-2 + - 2": -4,
        "-6 / -3 * -4": -8,

        "-5": -5,
        "2-10": -8,

        "2 in [1..3]": 1,
        "2 in [3..4]": 0,
        "[3..5] in [1..6]": 1,
        "[3..5] in [7..8]": 0,
        "5 in 5": 1,
        "5 in 6": 0,

        "2 in 2 to 3": 1,
        "2 in 4 to 5": 0,
        "5 in [1..2] to [6..7]": 1,
        "5 in [6..7] to [4..4]": 1,
        "0 in [1..2] to [6..7]": 0,
        "8 in [1..2] to [6..7]": 0,

        "1 > 2": 0,
        "2 >= 2": 1,
        "2 >= 3": 0,
        "2 = 2": 1,
        "3 = 4": 0,
        " 5 < 1": 0,
        " 5 <= 4": 0,
        " 5 <= 5": 1,
        "6 <> 7": 1,
        "6 <> 6": 0,
        "1 and 1+1": 1,
        "1 or 0": 1,
        "10 or 11": 1,
        "0 and 0": 0,
        "3 and 0": 0,
        "0 and 3": 0,
        "0 or 0": 0,
        "0 or 4": 1,

        # /*
        #     '2 <> <>': 1,
        #     '100 <> <>': 0,
        #     '<> <> 2': 1,
        #     '<> <> 100': 0,
        #
        #     //'<> <> <> + 1': 1,
        #     '<> <> <>': 0,
        #     '<> mod 11': 2,
        #     '<> <> <> and <> <> <>': 0,
        #     //'<> <> <> and <> <> <> or <> <> <> + 1': 1,
        #     */

        "2 <> 2": 0,
        "4 <> 5": 1,

        "2 + [p3] * 3": 8,
        "2 + [p4] * 3": 14,
        "[p1]+[p2]*[p3]+[p4]": 6,

        "[p3] in [p2] to [p4]": 1,
        "[p2] in [p3] to [p4]": 0,

        "[-2]": -2,

        "[-3;-3;-3..-3]": -3,

        "0.05*100": 5,
        "100*0.05": 5,
        "10 000 + 1 00": 10100,
    }
    params = ParamValues([0, 1, 2, 4, 8, 16, 32, 64, 100])
    for i in range(100):
        params.append(i * 2)

    for k, v in test_equations.items():
        log.info(f'Calculates {k} into {v}')
        assert calculate(k, rnd, params) == test_equations[k]

    for withRandom in ('[p48]+[0..1]*[0..1]*[-1..1]+([p48]=0)*[1..8]',
                       '[1..0]'):
        log.info(f'Calculates \'{withRandom}\'')
        calculate(withRandom, rnd, params)

    log.info('Formula with new lines')
    assert calculate(' 1 \n + \r\n 1', rnd, ParamValues()) == 2

    log.info('Calculates scary formula from Codebox')
    assert calculate('(-(([p4] div 1000) mod 10)*1000*(([p1] div 10)=1)-'
                     '(([p4] div 100) mod 10)*100*(([p1] div 10)=2)-'
                     '(([p4] div 10) mod 10)*10*(([p1] div 10)=3)-'
                     '(([p4] div 1) mod 10)*1*(([p1] div 10)=4))',
                     rnd,
                     ParamValues([44, 4631, 7584, 3152, 8270, 72])) == -2


def test_randomness_ranges():
    for i in range(10_000):
        val = calculate('3 + [4;9;  10..20]', rnd, ParamValues())
        assert val in (7, 12) or 13 <= val <= 23


def test_randomness_ranges_w_neg_values():
    for i in range(10_000):
        val = calculate('3 + [ -20..-10]', rnd, ParamValues())
        assert -20 + 3 <= val <= -10 + 3


def test_randomness_ranges_w_neg_reversed_values():
    for i in range(10_000):
        val = calculate('3 + [ -10 ..  -12; -3]', rnd, ParamValues())
        assert val == 0 or (-12 + 3 <= val <= -10 + 3)


def test_randomness_distribution():
    values = {}
    for i in range(10_000):
        val = calculate('3 + [1;3;6..9] - 3', rnd, ParamValues())
        assert val in (1, 3) or (6 <= val <= 9), f'Random value={val}'
        values[val] = values[val] + 1 if val in values else 0

    for x in values.keys():
        assert values[x] > (10_000 / 6) * 0.9, f'Values={values}'
        assert values[x] < (10_000 / 6) * 1.1, f'Values={values}'
