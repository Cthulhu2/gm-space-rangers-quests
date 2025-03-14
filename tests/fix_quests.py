import io
import logging
from os import listdir
from os.path import join

from srqmplayer.qmmodels import QM
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


def fix_prison1():
    # Fix: Prison1.qm w max money 10_000 -> 2_000_000_000
    for name in ('Prison1', 'Prison1_eng', 'Prison1_cze',
                 'Prison1_fra', 'Prison1_hun', 'Prison1_pol'):

        with open(join(QUEST_DIR, f'{name}.qm'), 'rb') as f:
            quest = parse(f)
            if quest.params[10].isMoney and quest.params[10].max == 10_000:
                quest.params[10].max = 2_000_000_000
                log.warning(f'{name}.qm p11 Max money 10 000 -> 2 000 000 000')
                with open(join(QUEST_DIR, f'{name}.qmm'), 'wb') as s:
                    packed = write_qmm(quest, io.BytesIO())
                    s.write(packed)


def _copy_loc_media_img(name: str, src: QM, dst: QM):
    fixed = False
    for src_loc in src.locations:
        dst_loc = dst.find_loc(src_loc.id)
        for i, src_loc_media in enumerate(src_loc.media):
            if dst_loc.media[i].img != src_loc_media.img:
                log.warning(f'{name} loc={dst_loc.id}'
                            f' media={i} img'
                            f' {dst_loc.media[i].img}'
                            f' -> {src_loc_media.img}')
                dst_loc.media[i].img = src_loc_media.img
                fixed = True
    return fixed


def _copy_jump_media_img(name: str, src: QM, dst: QM):
    fixed = False
    for src_jmp in src.jumps:
        dst_jmp = dst.find_jump(src_jmp.id)
        if not dst_jmp:
            log.warning(f'{name} no jump={src_jmp.id}!!!!!!!!')
            continue  # skip
        if dst_jmp.img != src_jmp.img:
            log.warning(f'{name} jump={dst_jmp.id} img'
                        f' {dst_jmp.img} -> {src_jmp.img}')
            dst_jmp.img = src_jmp.img
            fixed = True
    return fixed


def fix_qm_images():
    for name in (
            #'Boat', 'Build', 'Casino', 'Commando', 'Diehard', 'Energy',
            #'Fishing', 'Gladiator', 'Gobsaur', 'Hachball', 'Ikebana',
            #'Murder', 'Tomb'
            'Prison1', ):
        with open(join(QUEST_DIR, f'{name}.qmm'), 'rb') as f:
            ru = parse(f)

        for lang in ('eng', 'cze', 'fra', 'hun', 'pol'):
            with open(join(QUEST_DIR, f'{name}_{lang}.qmm'), 'rb') as f:
                eng = parse(f)

            loc_fixed = _copy_loc_media_img(f'{name}_{lang}.qmm', ru, eng)
            jmp_fixed = _copy_jump_media_img(f'{name}_{lang}.qmm', ru, eng)

            if loc_fixed or jmp_fixed:
                with open(join(QUEST_DIR, f'{name}_{lang}.qmm'), 'wb') as s:
                    packed = write_qmm(eng, io.BytesIO())
                    s.write(packed)
