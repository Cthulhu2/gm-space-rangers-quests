from pathlib import Path
from typing import Optional

from gmsrq import Config
from gmsrq.sqlstore import Ranger, Quest, QuestState, QuestCompleted
from gmsrq.utils import site_title, meta


def page_index(_, ranger: Optional[Ranger], lang: str, cfg: Config, root: Path):
    if not ranger:
        page = root.joinpath(lang, 'index.gmi')
    elif ranger.is_anon:
        page = index_anon(_, cfg, ranger, lang)
    else:
        page = index_ranger(_, cfg, ranger, lang)
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
    quest_urls = build_quest_urls(ansi, cfg, f'Quests :: SR 2 HD: A War Apart',
                                  completed, in_progress, quests)
    return quest_urls


def build_quest_urls_de(cfg, ranger):
    ansi = ranger.get_opts().ansi
    in_progress = QuestState.in_progress(rid=ranger.id)
    completed = QuestCompleted.by(rid=ranger.id)
    #
    quests = [q for q in Quest.all_by(lang='de', game='SR 2.1.2468 ger')]
    quest_urls = build_quest_urls(ansi, cfg, f'Quests :: SR 2 HD: A War Apart',
                                  completed, in_progress, quests)
    return quest_urls


def build_quest_urls_es(cfg, ranger):
    ansi = ranger.get_opts().ansi
    in_progress = QuestState.in_progress(rid=ranger.id)
    completed = QuestCompleted.by(rid=ranger.id)
    #
    quests = [q for q in Quest.all_by(lang='es', game='SR 2.1.2468 spa')]
    quest_urls = build_quest_urls(ansi, cfg, f'Quests :: SR 2 HD: A War Apart',
                                  completed, in_progress, quests)
    return quest_urls


def index_anon(_, cfg: Config, ranger: Ranger, lang):
    quest_urls = build_quest_urls_ru(cfg, ranger) if lang == 'ru' \
        else build_quest_urls_es(cfg, ranger) if lang == 'es' \
        else build_quest_urls_de(cfg, ranger) if lang == 'de' \
        else build_quest_urls_en(cfg, ranger)

    return (f'# {site_title(_)}\n' +
            _('Come in, ranger, your certificate is valid.') + '\n\n' +
            f'=> {cfg.reg_url} 🪪' + _('Registration') + '\n' +
            f'=> {cfg.opts_url} ⚙ ' + _('Options') + '\n' +
            f'=> /{lang}/leaders 💯 ' + _('Leader board') + '\n' +
            f'{quest_urls}\n' +
            footer(_, lang))


def index_ranger(_, cfg: Config, ranger: Ranger, lang):
    quest_urls = build_quest_urls_ru(cfg, ranger) if lang == 'ru' \
        else build_quest_urls_es(cfg, ranger) if lang == 'es' \
        else build_quest_urls_de(cfg, ranger) if lang == 'de' \
        else build_quest_urls_en(cfg, ranger)
    quest_completed = len(QuestCompleted.by(rid=ranger.id, lang=lang))
    quest_total = Quest.count_by(lang=lang)
    if ranger.get_opts().ansi:
        progress = f'\033[38;5;11m{quest_completed} / {quest_total}\033[0m'
        if lang == 'ru':
            credits = f'\033[38;5;11m{ranger.credits_ru}\033[0m'
        else:
            credits = f'\033[38;5;11m{ranger.credits_en}\033[0m'
    else:
        progress = f'{quest_completed} / {quest_total}'
        if lang == 'ru':
            credits = f'{ranger.credits_ru}'
        else:
            credits = f'{ranger.credits_en}'

    return (f'# {site_title(_)}\n' +
            _('Wow! This is the famous ranger {name}!')
            .format(name=ranger.name) + '\n\n' +
            _('Progress: ') + progress + '\n' +
            _('Credits: ') + credits + '\n\n' +
            f'=> {cfg.opts_url} ⚙ ' + _('Options') + '\n' +
            f'=> /{lang}/leaders 💯 ' + _('Leader board') + '\n' +
            f'{quest_urls}\n' +
            footer(_, lang))


def footer(_, lang):
    return (f'### ' + _('Info') + '\n' +
            f'=> /{lang}/gemlog/ ' + _('Gemlog') + '\n' +
            f'=> gemini://bbs.geminispace.org/s/SpaceRangers ' +
            _('Discuss on the BBS') + '\n' +
            f'=> https://github.com/Cthulhu2/gm-space-rangers-quests ' +
            _('Source code and Issues') + '\n' +
            f'=> misfin:cthulhu28@hashnix.club ' + _('Contact email (misfin)'))
