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


def fix_formulas_depth():
    # Expected close brace token but got 'durch' at 7
    with open(join(QUEST_DIR, 'Depth_ger.qmm'), 'rb') as f:
        quest = parse(f)
    loc = quest.find_loc(37)
    if '{([p11] durch 500 + 1) * 500}' in loc.texts[1]:
        loc.texts[1] = loc.texts[1].replace('{([p11] durch 500 + 1) * 500}',
                                            '{([p11] div 500 + 1) * 500}')
        with open(join(QUEST_DIR, 'Depth_ger.qmm'), 'wb') as s:
            packed = write_qmm(quest, io.BytesIO())
            s.write(packed)


def fix_formulas_driver():
    # Expecting primary value at 23 but got 'Sin' kind=$SyntaxKind.IDENTIFIER
    with open(join(QUEST_DIR, 'Driver_spa.qmm'), 'rb') as f:
        quest = parse(f)
    loc = quest.find_loc(122)
    if '{([p6]>300)*1500+([p6]<=Sin ' in loc.texts[0]:
        loc.texts[0] = loc.texts[0].replace(
            'Not waiting for her to repeat the offer you gave all you platinum'
            ' pieces to her. These were completely useless anywhere else in the'
            ' Galaxy. In return Ramina gave you the regular Galactic credits - '
            '{([p6]>300)*1500+([p6]<=Sin esperar a que ella repitiera la ',
            #
            'Sin esperar a que ella repitiera la '
        )
        with open(join(QUEST_DIR, 'Driver_spa.qmm'), 'wb') as s:
            packed = write_qmm(quest, io.BytesIO())
            s.write(packed)


def fix_formulas_olympiada():
    # Expecting primary value at 28 but got 'Bueno' kind=$SyntaxKind.IDENTIFIER
    with open(join(QUEST_DIR, 'Olympiada_spa.qmm'), 'rb') as f:
        quest = parse(f)
    jmp = quest.find_jump(228)
    if '{(([p18] div 100 mod 100)>=- Bueno, ' in jmp.description:
        jmp.description = jmp.description.replace(
            "- Well, do you need it that bad? OK, I'll tell you. According to"
            " the results of my testing, <clr>the general IQ of your protégé is"
            " <clrEnd> {(([p18] div 100 mod 100)>=- Bueno, ",
            #
            '- Bueno, '
        )
        with open(join(QUEST_DIR, 'Olympiada_spa.qmm'), 'wb') as s:
            packed = write_qmm(quest, io.BytesIO())
            s.write(packed)


def fix_formulas_pilot():
    # Expecting primary value at 26 but got 'La' kind=$SyntaxKind.IDENTIFIER
    with open(join(QUEST_DIR, 'Pilot_spa.qmm'), 'rb') as f:
        quest = parse(f)
    jmp = quest.find_jump(286)
    if '{10*([p21]+21)+30*([p21]=- La respuesta ' in jmp.description:
        jmp.description = jmp.description.replace(
            '- Correct answer is {10*([p21]+21)+30*([p21]=- La respuesta ',
            '- La respuesta '
        )
        with open(join(QUEST_DIR, 'Pilot_spa.qmm'), 'wb') as s:
            packed = write_qmm(quest, io.BytesIO())
            s.write(packed)


def fix_formulas_sashki():
    # Unknown char '.' at 5 in '[5 ... 20]'
    with open(join(QUEST_DIR, 'Shashki_ger.qmm'), 'rb') as f:
        quest = parse(f)
    loc = quest.find_loc(10)

    if 'vor {[5 ... 20]} Jahren' in loc.texts[5]:
        loc.texts[5] = loc.texts[5].replace('{[5 ... 20]}',
                                            '{[5..20]}')
        with open(join(QUEST_DIR, 'Shashki_ger.qmm'), 'wb') as s:
            packed = write_qmm(quest, io.BytesIO())
            s.write(packed)
