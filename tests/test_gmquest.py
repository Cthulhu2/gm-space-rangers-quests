import logging
from os import listdir
from os.path import join
from unittest.mock import MagicMock

from gmsrq.gmquests import find_format_tag, FormatToken, choice_planets
from srqmplayer.qmmodels import Race
from srqmplayer.qmreader import parse
# noinspection PyUnresolvedReferences
from . import temp_db
from .test_20_quests_formula_and_substitution import BORROWED_QUEST_DIR

log = logging.getLogger()


def test_find_format_tag():
    tag = find_format_tag('<format=center,   40>body</format>')
    assert tag == FormatToken(beginIdx=0, endIdx=34, body='body',
                              padding='center', paddingSize=40)

    tag = find_format_tag('<format=center, 41>body</format>')
    assert tag == FormatToken(beginIdx=0, endIdx=32, body='body',
                              padding='center', paddingSize=41)

    tag = find_format_tag('<format=left,20>body</format>')
    assert tag == FormatToken(beginIdx=0, endIdx=29, body='body',
                              padding='left', paddingSize=20)

    tag = find_format_tag('no format')
    assert not tag


def test_choice_planets(temp_db):
    qm = MagicMock()
    qm.givingRace = Race.People
    qm.planetRace = Race.People
    f_star, f_planet, to_star, to_planet = choice_planets('ru', qm)
    assert f_star
    assert f_planet
    assert to_star
    assert to_planet


def test_choice_planets_quests(temp_db):
    for f in listdir(BORROWED_QUEST_DIR):
        if not f.endswith('.qm') and not f.endswith('.qmm'):
            continue
        with open(join(BORROWED_QUEST_DIR, f), 'rb') as data:
            qm = parse(data)
        log.info(f)
        for lang in ('en', 'ru', 'es', 'de'):
            f_star, f_planet, to_star, to_planet = choice_planets(lang, qm)
            assert f_star, f'{lang} :: {f}'
            assert f_planet, f'{lang} :: {f}'
            assert to_star, f'{lang} :: {f}'
            assert to_planet, f'{lang} :: {f}'


def xtest_difficulty():
    strings = []
    for f in listdir(BORROWED_QUEST_DIR):
        if not f.endswith('.qm') and not f.endswith('.qmm'):
            continue
        with open(join(BORROWED_QUEST_DIR, f), 'rb') as data:
            qm = parse(data)
        strings.append(f'{f} :: {qm.hardness}')
    strings.sort()
    for s in strings:
        log.info(s)
