from pathlib import Path
from typing import Optional, List, Tuple

from gmsrq import Config
from gmsrq.sqlstore import (
    Ranger, Quest, QuestState, QuestCompleted, Duration, Genre, SortType,
    SortDirection
)
from gmsrq.utils import site_title, meta


def page_index(_, ranger: Optional[Ranger], lang: str, cfg: Config, root: Path):
    if not ranger:
        page = root.joinpath(lang, 'index.gmi')
    elif ranger.is_anon:
        page = index_anon(_, cfg, ranger, lang)
    else:
        page = index_ranger(_, cfg, ranger, lang)
    return 20, meta(lang), page


def build_quest_url(_, q: Quest, cfg: Config, ansi, completed, in_progress):
    mark = '☑' if q.id in completed else '☐'
    url = f'=> {cfg.act_url}?qid={q.id} {mark} {q.name}'
    if q.id in in_progress:
        url += ' \033[38;5;10m(in progress)\033[0m' if ansi \
            else ' (in progress)'
    if q.difficult or q.duration or q.genre:
        url += '\n' + ' '.join((build_difficult(q),
                                build_duration(_, q),
                                build_genre(_, q))).strip()
    return url


def build_quest_urls(_, ansi, cfg: Config, title, completed, in_progress,
                     quests):
    game_completed = list(filter(lambda qid: qid in completed,
                                 map(lambda q: q.id, quests)))
    game_urls = '\n'.join(
        build_quest_url(_, quest, cfg, ansi, game_completed, in_progress)
        for quest in quests)

    return f'## {title} ({len(game_completed)} / {len(quests)})\n' \
           f'{game_urls}\n'


def build_quest_urls_ru(cfg, ranger):
    ansi = ranger.get_opts().ansi
    _ = cfg.l10n['ru'].gettext
    sort_type = ranger.get_opts().sort_type
    sort_dir = ranger.get_opts().sort_dir
    in_progress = QuestState.in_progress(rid=ranger.id)
    completed = QuestCompleted.by(rid=ranger.id)
    quest_urls = ''
    #
    quests = [q for q in Quest.all_by(lang='ru', game='КР 1',
                                      sort_type=sort_type, sort_dir=sort_dir)]
    quest_urls += build_quest_urls(
        _, ansi, cfg, _('Quests :: {game}').format(game='КР 1'),
        completed, in_progress, quests)
    #
    quests = [q for q in Quest.all_by(lang='ru', game='КР 2 Доминаторы',
                                      sort_type=sort_type, sort_dir=sort_dir)]
    quest_urls += build_quest_urls(
        _, ansi, cfg, _('Quests :: {game}').format(game='КР 2 Доминаторы'),
        completed, in_progress, quests)
    #
    quests = [q for q in Quest.all_by(
        lang='ru', game='КР 2 Доминаторы: Перезагрузка',
        sort_type=sort_type, sort_dir=sort_dir)]
    quest_urls += build_quest_urls(
        _, ansi, cfg,
        _('Quests :: {game}').format(game='КР 2 Доминаторы: Перезагрузка'),
        completed, in_progress, quests)
    # КР 2 Доминаторы HD Революция
    sr2r_orig = [q for q in Quest.all_by(
        lang='ru', game='КР HD: Революция Оригинальные',
        sort_type=sort_type, sort_dir=sort_dir)]
    sr2r_orig_completed = list(filter(lambda qid: qid in completed,
                                      map(lambda q: q.id, sr2r_orig)))
    sr2r_fan = [q for q in Quest.all_by(
        lang='ru', game='КР HD: Революция Фанатские',
        sort_type=sort_type, sort_dir=sort_dir)]
    sr2r_fan_completed = list(filter(lambda qid: qid in completed,
                                     map(lambda q: q.id, sr2r_fan)))
    quest_urls += f'## ' + \
                  _('Quests :: {game}').format(game='КР HD: Революция') + \
                  f' ({len(sr2r_orig_completed) + len(sr2r_fan_completed)}' \
                  f' / {len(sr2r_orig) + len(sr2r_fan)})\n' \
                  f'### Оригинальные\n'
    quest_urls += '\n'.join(build_quest_url(_, quest, cfg, ansi,
                                            sr2r_orig_completed, in_progress)
                            for quest in sr2r_orig)
    quest_urls += '\n### Фанатские\n'
    quest_urls += '\n'.join(build_quest_url(_, quest, cfg, ansi,
                                            sr2r_fan_completed, in_progress)
                            for quest in sr2r_fan)
    # Фанатские
    quest_urls += '\n'
    quests = [q for q in Quest.all_by(lang='ru', game='Фанатские',
                                      sort_type=sort_type, sort_dir=sort_dir)]
    quest_urls += build_quest_urls(_, ansi, cfg, _('Quests :: {game}').format(game='Фанатские'),
                                   completed, in_progress, quests)
    return quest_urls


def build_quest_urls_xx(cfg, ranger, lang, game_title: List[Tuple[str, str]]):
    ansi = ranger.get_opts().ansi
    _ = cfg.l10n[lang].gettext
    sort_type = ranger.get_opts().sort_type
    sort_dir = ranger.get_opts().sort_dir
    in_progress = QuestState.in_progress(rid=ranger.id)
    completed = QuestCompleted.by(rid=ranger.id)
    #
    quest_urls = ''
    for game, title in game_title:
        quests = [q for q in Quest.all_by(lang=lang, game=game,
                                          sort_type=sort_type,
                                          sort_dir=sort_dir)]
        quest_urls += build_quest_urls(
            _, ansi, cfg, _('Quests :: {game}').format(game=title),
            completed, in_progress, quests)
        quest_urls += '\n'
    return quest_urls


QUEST_FILTER = {
    # TODO: Refactor quest filtering with 3-rd level subtitles
    'ru': [('КР 1', 'КР 1'),
           ('КР 2 Доминаторы', 'КР 2 Доминаторы'),
           ('КР 2 Доминаторы: Перезагрузка', 'КР 2 Доминаторы: Перезагрузка'),
           ('КР HD: Революция Оригинальные', 'КР HD: Революция (Оригинальные)'),
           ('КР HD: Революция Фанатские', 'КР HD: Революция (Фанатские)')],
    'en': [('SR 1.7.2', 'SR 1'),
           ('SR 2.1.2468 eng', 'SR HD: A War Apart')],
    'es': [('SR 2.1.2468 spa', 'SR HD: A War Apart')],
    'de': [('SR 2.1.2468 ger', 'SR HD: A War Apart')],
    'cze': [('SR 1.7.2', 'SR 1')],
    'fr': [('SR 1.7.2', 'SR 1')],
    'hu': [('SR 1.7.2', 'SR 1')],
    'pl': [('SR 1.7.2', 'SR 1')]
}


def index_anon(_, cfg: Config, ranger: Ranger, lang):
    quest_urls = build_quest_urls_ru(cfg, ranger) if lang == 'ru' \
        else build_quest_urls_xx(cfg, ranger, lang, QUEST_FILTER[lang])

    sort_urls = build_sort_urls(_, cfg, ranger)

    return (f'# {site_title(_)}\n' +
            _('Come in, ranger, your certificate is valid.') + '\n\n' +
            f'=> {cfg.reg_url} 🪪' + _('Registration') + '\n' +
            f'=> {cfg.opts_url} ⚙ ' + _('Options') + '\n' +
            f'=> /{lang}/leaders 💯 ' + _('Leader board') + '\n' +
            f'=> /{lang}/about.gmi ℹ ' + _('About') + '\n' +
            f'\n' + sort_urls +
            f'{quest_urls}\n')


def color(text):
    return f'\033[38;5;11m{text}\033[0m'


def index_ranger(_, cfg: Config, ranger: Ranger, lang):
    quest_urls = build_quest_urls_ru(cfg, ranger) if lang == 'ru' \
        else build_quest_urls_xx(cfg, ranger, lang, QUEST_FILTER[lang])
    quest_completed = len(QuestCompleted.by(rid=ranger.id, lang=lang))
    quest_total = Quest.count_by(lang=lang)
    if ranger.get_opts().ansi:
        progress = color(f'{quest_completed} / {quest_total}')
        credits = color(ranger.get_credits(lang))
    else:
        progress = f'{quest_completed} / {quest_total}'
        credits = f'{ranger.get_credits(lang)}'

    sort_urls = build_sort_urls(_, cfg, ranger)

    return (f'# {site_title(_)}\n' +
            _('Wow! This is the famous ranger {name}!')
            .format(name=ranger.name) + '\n\n' +
            _('Progress: ') + progress + '\n' +
            _('Credits: ') + credits + '\n\n' +
            f'=> {cfg.opts_url} ⚙ ' + _('Options') + '\n' +
            f'=> /{lang}/leaders 💯 ' + _('Leader board') + '\n' +
            f'=> /{lang}/about.gmi ℹ ' + _('About') + '\n' +
            f'\n' + sort_urls +
            f'{quest_urls}\n')


def build_sort_urls(_, cfg, ranger: Ranger):
    st = ranger.get_opts().sort_type
    difficult = _('☠ difficulty')
    duration = _('⏱ duration')
    genre = _('🏷 genre')
    type_url = (f'=> {cfg.sort_url}?type ⇵ \u200B' + ' '.join((
        f' [[ {difficult} ]] ' if st == SortType.DIFFICULT else difficult,
        f' [[ {duration} ]] ' if st == SortType.DURATION else duration,
        f' [[ {genre} ]] ' if st == SortType.GENRE else genre)))

    sd = ranger.get_opts().sort_dir
    asc = _('⬆ ascend')
    desc = _('⬇ descend')
    dir_url = (f'=> {cfg.sort_url}?dir ⇵ \u200B' + ' '.join((
        f' [[ {asc} ]] ' if sd == SortDirection.ASCEND else asc,
        f' [[ {desc} ]] ' if sd == SortDirection.DESCEND else desc)))

    return f'{type_url}\n{dir_url}\n'


def build_difficult(q: Quest):
    if q.difficult:
        return f'☠ {q.difficult}%'
    return ''


def build_duration(_, q: Quest):
    if q.duration is None:
        return ''
    if q.duration == Duration.LOW:
        return _('⏱ low')
    elif q.duration == Duration.BELOW_AVERAGE:
        return _('⏱ below average')
    elif q.duration == Duration.AVERAGE:
        return _('⏱ average')
    elif q.duration == Duration.ABOVE_AVERAGE:
        return _('⏱ above average')
    elif q.duration == Duration.LONG:
        return _('⏱ long')
    return ''


def build_genre(_, q: Quest):
    if q.genre is None:
        return ''
    # TODO: Fix gettext w multi-threaded/multiuser n refactor if-else w dict
    if q.genre == Genre.ADVENTURE:
        return _('🏷 adventure')
    elif q.genre == Genre.ADVENTURE_SHOOTER:
        return _('🏷 adventure-shooter')
    elif q.genre == Genre.ADVENTURE_SHOOTER_SAFE_CRACK_SIM:
        return _('🏷 adventure-shooter; safe cracking simulator')
    elif q.genre == Genre.ADVENTURE_W_ADVENTURES:
        return _('🏷 adventure with adventures')
    elif q.genre == Genre.ADVENTURE_W_ARCADE_ELEMENTS:
        return _('🏷 adventure with arcade elements')
    elif q.genre == Genre.ADVENTURE_W_BLACK_HUMOR_ELEMENTS:
        return _('🏷 adventure with black humor elements')
    elif q.genre == Genre.ADVENTURE_W_FIGHTING_ELEMENTS:
        return _('🏷 adventure with fighting elements')
    elif q.genre == Genre.ADVENTURE_W_FIGHTING_N_PUZZLE_ELEMENTS:
        return _('🏷 adventure with fighting and puzzle elements')
    elif q.genre == Genre.ADVENTURE_W_MANAGEMENT_ELEMENTS:
        return _('🏷 adventure with management elements')
    elif q.genre == Genre.ADVENTURE_W_HORROR_ELEMENTS:
        return _('🏷 adventure with horror elements')
    elif q.genre == Genre.ADVENTURE_W_AWFUL_HORROR_ELEMENTS:
        return _('🏷 adventure with awful horror elements')
    elif q.genre == Genre.ADVENTURE_W_LOGIC_ELEMENTS:
        return _('🏷 adventure with logic elements')
    elif q.genre == Genre.ADVENTURE_W_LOGIC_PUZZLES:
        return _('🏷 adventure with logic puzzles')
    elif q.genre == Genre.TRIVIA_GAME:
        return _('🏷 trivia game')
    elif q.genre == Genre.TEXT_AND_LOGIC_PUZZLE:
        return _('🏷 text and logic puzzle')
    elif q.genre == Genre.PUZZLE:
        return _('🏷 puzzle')
    elif q.genre == Genre.LOGIC_PUZZLE:
        return _('🏷 logic puzzle')
    elif q.genre == Genre.ARCADE_LOGIC_GAME:
        return _('🏷 arcade logic game')
    elif q.genre == Genre.LOGIC_GAME:
        return _('🏷 logic game')
    elif q.genre == Genre.LOGIC_GAME_W_MANAGEMENT_ELEMENTS:
        return _('🏷 logic game with management elements')
    elif q.genre == Genre.LOGIC_EDUCATIONAL_GAME:
        return _('🏷 logic educational game')
    elif q.genre == Genre.LOGIC_MATH_GAME:
        return _('🏷 logic math game')
    elif q.genre == Genre.LOGIC_EASEL_SIMULATOR:
        return _('🏷 logic easel simulator')
    elif q.genre == Genre.MATH_LOGIC_PUZZLE:
        return _('🏷 math logic puzzle')
    elif q.genre == Genre.MATH_PUZZLE:
        return _('🏷 math puzzle')
    elif q.genre == Genre.LOGIC_PUZZLES_AND_MATH_PROBLEMS:
        return _('🏷 logic puzzles and math problems')
    elif q.genre == Genre.LOGIC_TACTICAL_GAME:
        return _('🏷 logic tactical game')
    elif q.genre == Genre.SIMULATOR:
        return _('🏷 simulator')
    elif q.genre == Genre.PRISON_SIM:
        return _('🏷 prison simulator')
    elif q.genre == Genre.SPACE_RANGERS_SIM:
        return _('🏷 space rangers simulator')
    elif q.genre == Genre.ANIMAL_LIFE_SIM:
        return _('🏷 animal life simulator')
    elif q.genre == Genre.LAB_RAT_SIM:
        return _('🏷 lab rat simulator')
    elif q.genre == Genre.COMPOSITE_SKETCH_SIM:
        return _('🏷 composite sketch simulator')
    elif q.genre == Genre.ECONOMY_SIM:
        return _('🏷 economy simulator')
    elif q.genre == Genre.ELECTION_CAMPAIGN_SIM:
        return _('🏷 election campaign simulator')
    elif q.genre == Genre.HAULER_SIM:
        return _('🏷 hauler simulator')
    elif q.genre == Genre.TAXI_SIM:
        return _('🏷 taxi simulator')
    elif q.genre == Genre.FISHING_SIM:
        return _('🏷 fishing simulator')
    elif q.genre == Genre.ANCIENT_CARS_RACING_SIM:
        return _('🏷 ancient cars racing simulator')
    elif q.genre == Genre.RACING_SIM:
        return _('🏷 racing simulator')
    elif q.genre == Genre.RACING_SIM_W_MANAGEMENT_ELEMENTS:
        return _('🏷 racing simulator with management elements')
    elif q.genre == Genre.PENCHEKRACK_BREEDING_SIM:
        return _('🏷 penchekrack breeding simulator')
    elif q.genre == Genre.WILD_GOBZAUR_TAMING_SIM:
        return _('🏷 wild gobzaur taming simulator')
    elif q.genre == Genre.PASSING_ENTRANCE_EXAMS:
        return _('🏷 passing entrance exams')
    elif q.genre == Genre.TACTICAL_FIGHTING:
        return _('🏷 tactical fighting')
    elif q.genre == Genre.TACTICAL_GAME:
        return _('🏷 tactical game')
    elif q.genre == Genre.TACTICAL_STRATEGY:
        return _('🏷 tactical strategy')
    elif q.genre == Genre.ECONOMIC_STRATEGY:
        return _('🏷 economic strategy')
    elif q.genre == Genre.STRATEGY_W_FIGHTING_ELEMENTS:
        return _('🏷 strategy with fighting elements')
    elif q.genre == Genre.RECRUITMENT_CENTER_MANAGER:
        return _('🏷 recruitment center manager')
    elif q.genre == Genre.MANAGEMENT:
        return _('🏷 management')
    elif q.genre == Genre.BUILD_MANAGEMENT:
        return _('🏷 build management')
    elif q.genre == Genre.SPORT_MANAGEMENT:
        return _('🏷 sport management')
    elif q.genre == Genre.GAMBLING:
        return _('🏷 gambling')
    elif q.genre == Genre.TRADING:
        return _('🏷 trading')
    elif q.genre == Genre.WEAPONS_TESTING:
        return _('🏷 weapons testing')
    elif q.genre == Genre.ESPIONAGE:
        return _('🏷 espionage')
    elif q.genre == Genre.ESPIONAGE_GAMBLING:
        return _('🏷 espionage; gambling')
    elif q.genre == Genre.ESPIONAGE_BUGGING:
        return _('🏷 espionage; bugging')
    elif q.genre == Genre.ASSAULT:
        return _('🏷 assault')
    elif q.genre == Genre.FANTASY_ROLE_PLAYING_GAME:
        return _('🏷 fantasy role-playing game')
    elif q.genre == Genre.DETECTIVE:
        return _('🏷 detective')
    elif q.genre == Genre.HUMOROUS_DETECTIVE:
        return _('🏷 humorous detective')
    elif q.genre == Genre.CARGO_DELIVERY_W_QUEST_ELEMENTS:
        return _('🏷 cargo delivery with quest elements')
    elif q.genre == Genre.FORTRESS_DEFEND:
        return _('🏷 fortress defend')
    elif q.genre == Genre.ACTION_HORROR:
        return _('🏷 action horror')
    return ''
