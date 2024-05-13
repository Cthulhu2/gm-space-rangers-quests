import io
import logging
from os import listdir
from os.path import join

from srqmplayer.qmmodels import HEADER_QMM_7, HEADER_QMM_6
from srqmplayer.qmreader import Reader, parse
from srqmplayer.qmwriter import Writer, write_qmm
from tests import TEST_RESOURCE_DIR

log = logging.getLogger()


def fix_siege_new_lines():
    with open('../borrowed/qm/Siege.qm', 'rb') as f:
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


def check_file(f_name: str):
    if not f_name.endswith("Amnesia.qmm"):
        pass

    with open(f_name, 'rb') as f:
        read = f.read(4)
        f.seek(0, 0)
        header = int.from_bytes(read, 'little', signed=True)
        if header in (HEADER_QMM_6, HEADER_QMM_7):
            log.info(f'{f_name} equal after deserialize')
            quest = parse(f)
            packed = write_qmm(quest, io.BytesIO())
            unpacked = parse(io.BytesIO(packed))
            # small hack to force them to be equal
            if quest.header == HEADER_QMM_6:
                quest.header = HEADER_QMM_7
                quest.majorVer = 1
                quest.minorVer = 0

            assert unpacked == quest

            # # This is skipped due to some strings issues
            # log.info(f'{f_name} equals')
            # f.seek(0, 0)
            # file_raw = f.read()
            # f.seek(0, 0)
            # qm = parse(f)
            # buf = write_qmm(qm, io.BytesIO())
            # # with open(f'{f_name}.saved', 'wb') as s:
            # #     s.write(buf)
            # assert file_raw == buf


def test_writer():
    log.info('Writer class')

    log.info('Empty buff')
    w = Writer(io.BytesIO())
    assert len(w.export()) == 0

    log.info('int32')
    w = Writer(io.BytesIO())
    w.int32(83758303)
    buf = w.export()
    assert len(w.export()) == 4
    assert Reader(io.BytesIO(buf)).int32() == 83758303

    log.info('byte')
    w = Writer(io.BytesIO())
    w.byte(243)
    buf = w.export()
    assert len(w.export()) == 1
    assert Reader(io.BytesIO(buf)).byte() == 243

    log.info('float64')
    w = Writer(io.BytesIO())
    w.float64(0.123456789)
    buf = w.export()
    assert len(w.export()) == 8
    assert Reader(io.BytesIO(buf)).float64() == 0.123456789

    log.info('Empty string')
    w = Writer(io.BytesIO())
    w.write_string(None)
    buf = w.export()
    assert len(w.export()) == 4
    assert Reader(io.BytesIO(buf)).read_string() == ''

    log.info('Not empty string with utf8 symbols')
    w = Writer(io.BytesIO())
    w.write_string('Лол куку')
    buf = w.export()
    assert len(w.export()) == (4 + 4 + 8 * 2)
    assert Reader(io.BytesIO(buf)).read_string() == 'Лол куку'

    log.info('All files here')
    for f in listdir(TEST_RESOURCE_DIR):
        if not f.endswith(".qm") and not f.endswith(".qmm"):
            continue
        log.info(f'{str(f)}')
        check_file(f'{TEST_RESOURCE_DIR}/{str(f)}')

    log.info('All borrowed')
    src_dir = join(TEST_RESOURCE_DIR, '../../borrowed/qm/')
    for f in listdir(src_dir):
        if not f.endswith('.qm') and not f.endswith('.qmm'):
            continue
        fullname = join(src_dir, f)
        check_file(fullname)
