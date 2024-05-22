from unittest.mock import MagicMock

from gmsrq.gmquests import find_format_tag, FormatToken, choice_planets
from srqmplayer.qmmodels import Race
# noinspection PyUnresolvedReferences
from . import temp_db


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
