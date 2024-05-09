from pathlib import Path
from typing import Optional

from gmsrq.sqlstore import Ranger


def meta(lang):
    return f'text/gemini; charset=utf-8; lang={lang}'


def page_index(ranger: Optional[Ranger], lang: str, root: Path):
    if lang == 'ru':
        if not ranger:
            page = root.joinpath(lang, 'index.gmi')
        elif ranger.is_anon:
            page = root.joinpath(lang, 'index.gmi')
        else:
            page = root.joinpath(lang, 'index.gmi')
    else:
        if not ranger:
            page = root.joinpath(lang, 'index.gmi')
        elif ranger.is_anon:
            page = root.joinpath(lang, 'index.gmi')
        else:
            page = root.joinpath(lang, 'index.gmi')
    return 20, meta(lang), page


# TODO: Render ranger quest progress
def index_anon_ru(ranger: Ranger):
    return ''


def index_anon_en(ranger: Ranger):
    return ''


def index_ranger_ru(ranger: Ranger):
    return ''


def index_ranger_en(ranger: Ranger):
    return ''
