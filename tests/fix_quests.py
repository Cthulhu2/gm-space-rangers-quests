import io
import logging
from os import listdir
from os.path import join

from srqmplayer.qmreader import parse
from srqmplayer.qmwriter import write_qmm
from tests import QUEST_DIR

log = logging.getLogger()


def fix_siege_new_lines():
    with open('Siege.qm', 'rb') as f:
        f.seek(0, 0)
        quest = parse(f)
        for i, x in enumerate(range(ord('A'), ord('I'))):
            quest.params[12].showingInfo[i].str = (
                f'-------------------------------------------------------\n'
                f'Стрельба в квадрат {chr(x)}{{<> mod 10}} по Гауссу\n'
                f'-------------------------------------------------------')
        quest.params[13].showingInfo[0].str = ('__________________________\n'
                                               'Состояние:')
        with open('../borrowed/qm/Siege.qmm', 'wb') as s:
            packed = write_qmm(quest, io.BytesIO())
            s.write(packed)


def test_format_tag():
    for fname in listdir(QUEST_DIR):
        if not fname.endswith('.qm') and not fname.endswith('.qmm'):
            continue
        with open(join(QUEST_DIR, fname), 'rb') as f:
            quest = parse(f)

        for i, loc in enumerate(quest.locations):
            for j, txt in enumerate(loc.texts):
                assert '<format=<format=' not in txt, \
                    f'{fname} loc={loc.id} text={j + 1} :: {txt}'


def fix_format_tag():
    for fname in listdir(QUEST_DIR):
        if not fname.endswith('.qm') and not fname.endswith('.qmm'):
            continue
        with open(join(QUEST_DIR, fname), 'rb') as f:
            quest = parse(f)
        patched = False
        for i, loc in enumerate(quest.locations):
            for j, txt in enumerate(loc.texts):
                while '<format=<format=' in txt:
                    txt = txt.replace('<format=<format=', '<format=')
                    loc.texts[j] = txt
                    log.warning(f'{fname} loc={loc.id} text={j + 1}'
                                f' :: fix format tag')
                    patched = True
        if patched:
            qname = '.'.join(fname.split('.')[:-1])
            with open(join(QUEST_DIR, f'{qname}.qmm'), 'wb') as f:
                packed = write_qmm(quest, io.BytesIO())
                f.write(packed)
