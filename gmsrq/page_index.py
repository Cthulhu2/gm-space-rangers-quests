from pathlib import Path
from typing import Optional

from gmsrq import Config
from gmsrq.sqlstore import Ranger, Quest, QuestState, QuestCompleted

TITLE_EN = '# Ranger Center "Union"\n'
TITLE_RU = '# Центр рейнджеров "Союз"\n'

FOOTER_EN = (
    f'### Info\n'
    f'=> gemini://bbs.geminispace.org/s/SpaceRangers Discuss on the BBS\n'
    f'=> https://github.com/Cthulhu2/gm-space-rangers-quests'
    f' Source code and Issues\n')

FOOTER_RU = (
    f'### Info\n'
    f'=> gemini://bbs.geminispace.org/s/SpaceRangers Обсудить на BBS\n'
    f'=> https://github.com/Cthulhu2/gm-space-rangers-quests'
    f' Исходники и ишьюсы\n')


def meta(lang):
    return f'text/gemini; charset=utf-8; lang={lang}'


def page_index(ranger: Optional[Ranger], lang: str, cfg: Config, root: Path):
    if lang == 'ru':
        if not ranger:
            page = root.joinpath(lang, 'index.gmi')
        elif ranger.is_anon:
            page = index_anon_ru(cfg, ranger)
        else:
            page = index_ranger_ru(cfg, ranger)
    else:
        if not ranger:
            page = root.joinpath(lang, 'index.gmi')
        elif ranger.is_anon:
            page = index_anon_en(cfg, ranger)
        else:
            page = index_ranger_en(cfg, ranger)
    return 20, meta(lang), page


def build_quest_url(q: Quest, cfg: Config, ansi, completed, in_progress):
    mark = '☑' if q.id in completed else '☐'
    url = f'=> {cfg.act_url}?qid={q.id} {mark} {q.name}'
    if q.id in in_progress:
        url += ' \033[38;5;10m(in progress)\033[0m' if ansi \
            else ' (in progress)'
    return url


def build_quest_urls(ansi, cfg, title, completed, in_progress, quests):
    game_completed = list(filter(lambda qid: qid in completed,
                                 map(lambda q: q.id, quests)))
    game_urls = '\n'.join(
        build_quest_url(quest, cfg, ansi, game_completed, in_progress)
        for quest in quests)

    return f'### {title} ({len(game_completed)} / {len(quests)})\n' \
           f'{game_urls}\n'


def build_quest_urls_ru(cfg, ranger):
    ansi = ranger.get_opts().ansi
    in_progress = QuestState.in_progress(rid=ranger.id)
    completed = QuestCompleted.by(rid=ranger.id)
    quest_urls = ''
    #
    quests = [q for q in Quest.all_by(lang='ru', game='КР 1')]
    quest_urls += build_quest_urls(ansi, cfg, f'Квесты :: КР 1',
                                   completed, in_progress, quests)
    #
    quests = [q for q in Quest.all_by(lang='ru', game=['КР 2 Доминаторы',
                                                       'SR 2.1.2170'])]
    quest_urls += build_quest_urls(ansi, cfg, f'Квесты :: КР 2 Доминаторы',
                                   completed, in_progress, quests)
    #
    quests = [q for q in Quest.all_by(
        lang='ru', game='КР 2 Доминаторы Перезагрузка')]
    quest_urls += build_quest_urls(
        ansi, cfg, f'Квесты :: КР 2 Доминаторы: Перезагрузка',
        completed, in_progress, quests)
    # КР 2 Доминаторы HD Революция
    sr2r_orig = [q for q in Quest.all_by(
        lang='ru', game=['КР 2 Доминаторы HD Революция Оригинальные',
                         'КР 2 2.1.2369'])]
    sr2r_orig_completed = list(filter(lambda qid: qid in completed,
                                      map(lambda q: q.id, sr2r_orig)))
    sr2r_fan = [q for q in Quest.all_by(
        lang='ru', game='КР 2 Доминаторы HD Революция Фанатские')]
    sr2r_fan_completed = list(filter(lambda qid: qid in completed,
                                     map(lambda q: q.id, sr2r_fan)))
    quest_urls += f'### Квесты :: КР 2 HD: Революция' \
                  f' ({len(sr2r_orig_completed) + len(sr2r_fan_completed)}' \
                  f' / {len(sr2r_orig) + len(sr2r_fan)})\n' \
                  f'Оригинальные\n'
    quest_urls += '\n'.join(build_quest_url(quest, cfg, ansi,
                                            sr2r_orig_completed, in_progress)
                            for quest in sr2r_orig)
    quest_urls += '\nФанатские\n'
    quest_urls += '\n'.join(build_quest_url(quest, cfg, ansi,
                                            sr2r_fan_completed, in_progress)
                            for quest in sr2r_fan)
    # Фанатские
    quest_urls += '\n'
    quests = [q for q in Quest.all_by(lang='ru', game='Фанатские')]
    quest_urls += build_quest_urls(ansi, cfg, f'Квесты :: Фанатские',
                                   completed, in_progress, quests)
    return quest_urls


def build_quest_urls_en(cfg, ranger):
    ansi = ranger.get_opts().ansi
    in_progress = QuestState.in_progress(rid=ranger.id)
    completed = QuestCompleted.by(rid=ranger.id)
    #
    quests = [q for q in Quest.all_by(lang='en', game='SR 2.1.2121 eng')]
    quest_urls = build_quest_urls(ansi, cfg, f'Quests :: SR 2',
                                  completed, in_progress, quests)
    return quest_urls


def index_anon_ru(cfg: Config, ranger: Ranger):
    quest_urls = build_quest_urls_ru(cfg, ranger)

    return (
        f'{TITLE_RU}'
        f'Входи, рейнджер, твой сертификат прошёл проверку.\n'
        f'=> {cfg.reg_url} Регистрация\n'
        f'=> {cfg.opts_url} ⚙ Настройки\n'
        f'{quest_urls}'
        f'{FOOTER_RU}')


def index_anon_en(cfg: Config, ranger: Ranger):
    quest_urls = build_quest_urls_en(cfg, ranger)
    return (
        f'{TITLE_EN}'
        f'Come in, ranger, your certificate is valid.\n'
        f'=> {cfg.reg_url} Registration\n'
        f'=> {cfg.opts_url} ⚙ Options\n'
        f'{quest_urls}\n'
        f'{FOOTER_EN}')


def index_ranger_ru(cfg: Config, ranger: Ranger):
    quest_urls = build_quest_urls_ru(cfg, ranger)
    return (
        f'{TITLE_RU}'
        f'Ба! Да это же знаменитый рейнджер {ranger.name}!\n'
        f'=> {cfg.opts_url} ⚙ Настройки\n'
        f'{quest_urls}'
        f'{FOOTER_RU}')


def index_ranger_en(cfg: Config, ranger: Ranger):
    quest_urls = build_quest_urls_en(cfg, ranger)
    return (
        f'{TITLE_EN}'
        f'Wow! This is the famous ranger {ranger.name}!\n'
        f'=> {cfg.opts_url} ⚙ Options\n'
        f'{quest_urls}\n'
        f'{FOOTER_EN}')
