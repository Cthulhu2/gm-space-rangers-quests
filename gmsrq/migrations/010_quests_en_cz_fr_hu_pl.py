from enum import IntEnum, auto

import peewee as pw
from peewee_migrate import Migrator


class Quest(pw.Model):
    id = pw.IntegerField(primary_key=True)
    name = pw.CharField(max_length=128, null=False)
    file = pw.CharField(max_length=128, null=False)
    lang = pw.CharField(max_length=5, null=False)
    gameVer = pw.CharField(max_length=128, null=False)
    genre = pw.SmallIntegerField(null=True)
    difficult = pw.SmallIntegerField(null=True)
    duration = pw.SmallIntegerField(null=True)

    class Meta:
        table_name = 'quest'


class Genre(IntEnum):
    # @formatter:off
    # Adventures
    ADVENTURE = auto()                               # бродилка
    ADVENTURE_SHOOTER = auto()                       # бродилка-стрелялка
    ADVENTURE_SHOOTER_SAFE_CRACK_SIM = auto()        # Бродилка-стрелялка; Симулятор взлома сейфа (КР1)
    ADVENTURE_W_ADVENTURES = auto()                  # бродилка с приключениями
    ADVENTURE_W_ARCADE_ELEMENTS = auto()             # бродилка с элементами аркады
    ADVENTURE_W_BLACK_HUMOR_ELEMENTS = auto()        # бродилка с элементами черного юмора
    ADVENTURE_W_FIGHTING_ELEMENTS = auto()           # бродилка с элементами файтинга
    ADVENTURE_W_FIGHTING_N_PUZZLE_ELEMENTS = auto()  # бродилка с элементами файтинга и головоломками
    ADVENTURE_W_MANAGEMENT_ELEMENTS = auto()         # бродилка с элементами менеджмента
    ADVENTURE_W_HORROR_ELEMENTS = auto()             # бродилка с элементами ужасов
    ADVENTURE_W_AWFUL_HORROR_ELEMENTS = auto()       # бродилка с элементами тихих ужасов
    ADVENTURE_W_LOGIC_ELEMENTS = auto()              # бродилка с логическими элементами
    ADVENTURE_W_LOGIC_PUZZLES = auto()               # бродилка с логическими головоломками
    # Logic
    TRIVIA_GAME = auto()                       # викторина
    TEXT_AND_LOGIC_PUZZLE = auto()             # текстово-логическая головоломка
    PUZZLE = auto()                            # Головоломка (КР1)
    LOGIC_PUZZLE = auto()                      # логическая головоломка
    ARCADE_LOGIC_GAME = auto()                 # аркадно-логическая игра
    LOGIC_GAME = auto()                        # логическая игра
    LOGIC_GAME_W_MANAGEMENT_ELEMENTS = auto()  # логическая игра с элементами менеджмента
    LOGIC_EDUCATIONAL_GAME = auto()            # логико-познавательная игра
    LOGIC_MATH_GAME = auto()                   # логико-математическая игра
    LOGIC_EASEL_SIMULATOR = auto()             # логический симулятор мольберта
    MATH_LOGIC_PUZZLE = auto()                 # логико-математическая головоломка
    MATH_PUZZLE = auto()                       # математическая головоломка
    LOGIC_PUZZLES_AND_MATH_PROBLEMS = auto()   # логические головоломки и математические задачи
    LOGIC_TACTICAL_GAME = auto()               # логико-тактическая игра
    # Simulators
    SIMULATOR = auto()                         # Симулятор (FANS)
    PRISON_SIM = auto()                        # симулятор тюрьмы
    SPACE_RANGERS_SIM = auto()                 # симулятор "космических рейнджеров"
    ANIMAL_LIFE_SIM = auto()                   # симулятор жизни животного
    LAB_RAT_SIM = auto()                       # Симулятор «подопытной крысы» (КР1)
    COMPOSITE_SKETCH_SIM = auto()              # симулятор составления фоторобота
    ECONOMY_SIM = auto()                       # экономический симулятор
    ELECTION_CAMPAIGN_SIM = auto()             # симулятор предвыборной кампании
    HAULER_SIM = auto()                        # симулятор дальнобойщика
    TAXI_SIM = auto()                          # симулятор таксиста
    FISHING_SIM = auto()                       # симулятор рыбалки
    ANCIENT_CARS_RACING_SIM = auto()           # Гонки на древних машинах (КР1)
    RACING_SIM = auto()                        # гоночный симулятор
    RACING_SIM_W_MANAGEMENT_ELEMENTS = auto()  # гоночный симулятор с элементами менеджмента
    PENCHEKRACK_BREEDING_SIM = auto()          # Симулятор выведения пенчекряка (КР1)
    WILD_GOBZAUR_TAMING_SIM = auto()           # Симулятор укрощения дикого гобзавра (КР1)
    PASSING_ENTRANCE_EXAMS = auto()            # Сдача вступительных экзаменов (КР1)
    # Strategies
    TACTICAL_FIGHTING = auto()             # тактический файтинг
    TACTICAL_GAME = auto()                 # тактическая игра
    TACTICAL_STRATEGY = auto()             # тактическая стратегия
    ECONOMIC_STRATEGY = auto()             # экономическая стратегия
    STRATEGY_W_FIGHTING_ELEMENTS = auto()  # стратегия с элементами файтинга
    RECRUITMENT_CENTER_MANAGER = auto()    # менеджер военкомата
    MANAGEMENT = auto()                    # Менеджмент (КР1)
    BUILD_MANAGEMENT = auto()              # Менеджмент; Управление стройкой (КР1)
    SPORT_MANAGEMENT = auto()              # Спорт-менеджер (КР1)
    # Others
    GAMBLING = auto()                         # Азартная игра (КР1)
    TRADING = auto()                          # Торговля (КР1)
    WEAPONS_TESTING = auto()                  # Испытание оружия (КР1)
    ESPIONAGE = auto()                        # Шпионаж (КР1)
    ESPIONAGE_GAMBLING = auto()               # Шпионаж; Азартные игры (КР1)
    ESPIONAGE_BUGGING = auto()                # Шпионаж; Установка жучков (КР1)
    ASSAULT = auto()                          # Штурм (КР1)
    FANTASY_ROLE_PLAYING_GAME = auto()        # фэнтезийная ролевая игра
    DETECTIVE = auto()                        # детектив
    HUMOROUS_DETECTIVE = auto()               # юмористический детектив
    CARGO_DELIVERY_W_QUEST_ELEMENTS = auto()  # доставка груза с элементами квеста
    FORTRESS_DEFEND = auto()                  # Защита крепости (КР1)
    ACTION_HORROR = auto()                    # Экшн с хоррором (FANS)
    # @formatter:on


class Duration(IntEnum):
    # @formatter:off
    LOW = 1            # низкая
    BELOW_AVERAGE = 2  # ниже средней
    AVERAGE = 3        # средняя
    ABOVE_AVERAGE = 4  # выше средней
    LONG = 5           # высокая
    # @formatter:on


QUEST_NAMES = [
    # @formatter:off
(209, 'cze', 'Boat_cze.qm',      'Loď',             'SR 1.7.2',  15, Duration.LOW,     Genre.PUZZLE                 ),  # noqa
(210, 'en',  'Boat_eng.qm',      'Boat',            'SR 1.7.2',  15, Duration.LOW,     Genre.PUZZLE                 ),  # noqa
(211, 'fr',  'Boat_fra.qm',      'Bateau',          'SR 1.7.2',  15, Duration.LOW,     Genre.PUZZLE                 ),  # noqa
(212, 'hu',  'Boat_hun.qm',      'Csónak',          'SR 1.7.2',  15, Duration.LOW,     Genre.PUZZLE                 ),  # noqa
(213, 'pl',  'Boat_pol.qm',      'Łódka',           'SR 1.7.2',  15, Duration.LOW,     Genre.PUZZLE                 ),  # noqa
(214, 'cze', 'Build_cze.qm',     'Konstrukce',      'SR 1.7.2',  50, Duration.LOW,     Genre.BUILD_MANAGEMENT       ),  # noqa
(215, 'en',  'Build_eng.qm',     'Construction',    'SR 1.7.2',  50, Duration.LOW,     Genre.BUILD_MANAGEMENT       ),  # noqa
(216, 'fr',  'Build_fra.qm',     'Construction',    'SR 1.7.2',  50, Duration.LOW,     Genre.BUILD_MANAGEMENT       ),  # noqa
(217, 'hu',  'Build_hun.qm',     'Építés',          'SR 1.7.2',  50, Duration.LOW,     Genre.BUILD_MANAGEMENT       ),  # noqa
(218, 'pl',  'Build_pol.qm',     'Budowa',          'SR 1.7.2',  50, Duration.LOW,     Genre.BUILD_MANAGEMENT       ),  # noqa
(219, 'cze', 'Casino_cze.qm',    'Kasino',          'SR 1.7.2',  50, Duration.LONG,    Genre.GAMBLING               ),  # noqa
(220, 'en',  'Casino_eng.qm',    'Casino',          'SR 1.7.2',  50, Duration.LONG,    Genre.GAMBLING               ),  # noqa
(221, 'fr',  'Casino_fra.qm',    'Casino',          'SR 1.7.2',  50, Duration.LONG,    Genre.GAMBLING               ),  # noqa
(222, 'hu',  'Casino_hun.qm',    'Kaszinó',         'SR 1.7.2',  50, Duration.LONG,    Genre.GAMBLING               ),  # noqa
(223, 'pl',  'Casino_pol.qm',    'Kasyno',          'SR 1.7.2',  50, Duration.LONG,    Genre.GAMBLING               ),  # noqa
(224, 'cze', 'Commando_cze.qm',  'Komando',         'SR 1.7.2',  50, Duration.AVERAGE, Genre.ASSAULT                ),  # noqa
(225, 'en',  'Commando_eng.qm',  'Commando',        'SR 1.7.2',  50, Duration.AVERAGE, Genre.ASSAULT                ),  # noqa
(226, 'fr',  'Commando_fra.qm',  'Commando',        'SR 1.7.2',  50, Duration.AVERAGE, Genre.ASSAULT                ),  # noqa
(227, 'hu',  'Commando_hun.qm',  'Kommandó',        'SR 1.7.2',  50, Duration.AVERAGE, Genre.ASSAULT                ),  # noqa
(228, 'pl',  'Commando_pol.qm',  'Komandos',        'SR 1.7.2',  50, Duration.AVERAGE, Genre.ASSAULT                ),  # noqa
(229, 'cze', 'Diehard_cze.qm',   'Hrozná smrt',     'SR 1.7.2',  10, Duration.LOW,     Genre.LAB_RAT_SIM            ),  # noqa
(230, 'en',  'Diehard_eng.qm',   'Horrible death',  'SR 1.7.2',  10, Duration.LOW,     Genre.LAB_RAT_SIM            ),  # noqa
(231, 'fr',  'Diehard_fra.qm',   'Mort horrible',   'SR 1.7.2',  10, Duration.LOW,     Genre.LAB_RAT_SIM            ),  # noqa
(232, 'hu',  'Diehard_hun.qm',   'Szörnyű halál',   'SR 1.7.2',  10, Duration.LOW,     Genre.LAB_RAT_SIM            ),  # noqa
(233, 'pl',  'Diehard_pol.qm',   'Straszna śmierć', 'SR 1.7.2',  10, Duration.LOW,     Genre.LAB_RAT_SIM            ),  # noqa
(234, 'cze', 'Energy_cze.qm',    'Energie',         'SR 1.7.2',  73, Duration.AVERAGE, Genre.LOGIC_PUZZLE           ),  # noqa
(235, 'en',  'Energy_eng.qm',    'Energy',          'SR 1.7.2',  73, Duration.AVERAGE, Genre.LOGIC_PUZZLE           ),  # noqa
(236, 'fr',  'Energy_fra.qm',    'Énergie',         'SR 1.7.2',  73, Duration.AVERAGE, Genre.LOGIC_PUZZLE           ),  # noqa
(237, 'hu',  'Energy_hun.qm',    'Energia',         'SR 1.7.2',  73, Duration.AVERAGE, Genre.LOGIC_PUZZLE           ),  # noqa
(238, 'pl',  'Energy_pol.qm',    'Energia',         'SR 1.7.2',  73, Duration.AVERAGE, Genre.LOGIC_PUZZLE           ),  # noqa
(239, 'cze', 'Fishing_cze.qm',   'Rybolov',         'SR 1.7.2',  50, Duration.LOW,     Genre.FISHING_SIM            ),  # noqa
(240, 'en',  'Fishing_eng.qm',   'Fishing',         'SR 1.7.2',  50, Duration.LOW,     Genre.FISHING_SIM            ),  # noqa
(241, 'fr',  'Fishing_fra.qm',   'Pêche',           'SR 1.7.2',  50, Duration.LOW,     Genre.FISHING_SIM            ),  # noqa
(242, 'hu',  'Fishing_hun.qm',   'Halászat',        'SR 1.7.2',  50, Duration.LOW,     Genre.FISHING_SIM            ),  # noqa
(243, 'pl',  'Fishing_pol.qm',   'Rybacki',         'SR 1.7.2',  50, Duration.LOW,     Genre.FISHING_SIM            ),  # noqa
(244, 'cze', 'Gladiator_cze.qm', 'Gladiátor',       'SR 1.7.2', 100, Duration.LOW,     Genre.MANAGEMENT             ),  # noqa
(245, 'en',  'Gladiator_eng.qm', 'Gladiator',       'SR 1.7.2', 100, Duration.LOW,     Genre.MANAGEMENT             ),  # noqa
(246, 'fr',  'Gladiator_fra.qm', 'Gladiateur',      'SR 1.7.2', 100, Duration.LOW,     Genre.MANAGEMENT             ),  # noqa
(247, 'hu',  'Gladiator_hun.qm', 'Gladiátor',       'SR 1.7.2', 100, Duration.LOW,     Genre.MANAGEMENT             ),  # noqa
(248, 'pl',  'Gladiator_pol.qm', 'Gladiator',       'SR 1.7.2', 100, Duration.LOW,     Genre.MANAGEMENT             ),  # noqa
(249, 'cze', 'Gobsaur_cze.qm',   'Gobsaur',         'SR 1.7.2',  10, Duration.LOW,     Genre.WILD_GOBZAUR_TAMING_SIM),  # noqa
(250, 'en',  'Gobsaur_eng.qm',   'Gobsaur',         'SR 1.7.2',  10, Duration.LOW,     Genre.WILD_GOBZAUR_TAMING_SIM),  # noqa
(251, 'fr',  'Gobsaur_fra.qm',   'Gobsaure',        'SR 1.7.2',  10, Duration.LOW,     Genre.WILD_GOBZAUR_TAMING_SIM),  # noqa
(252, 'hu',  'Gobsaur_hun.qm',   'Gobsaur',         'SR 1.7.2',  10, Duration.LOW,     Genre.WILD_GOBZAUR_TAMING_SIM),  # noqa
(253, 'pl',  'Gobsaur_pol.qm',   'Gobzaur',         'SR 1.7.2',  10, Duration.LOW,     Genre.WILD_GOBZAUR_TAMING_SIM),  # noqa
(254, 'cze', 'Hachball_cze.qm',  'Hachball',        'SR 1.7.2',  20, Duration.LOW,     Genre.SPORT_MANAGEMENT       ),  # noqa
(255, 'en',  'Hachball_eng.qm',  'Hachball',        'SR 1.7.2',  20, Duration.LOW,     Genre.SPORT_MANAGEMENT       ),  # noqa
(256, 'fr',  'Hachball_fra.qm',  'Comball',         'SR 1.7.2',  20, Duration.LOW,     Genre.SPORT_MANAGEMENT       ),  # noqa
(257, 'hu',  'Hachball_hun.qm',  'Hachball',        'SR 1.7.2',  20, Duration.LOW,     Genre.SPORT_MANAGEMENT       ),  # noqa
(258, 'pl',  'Hachball_pol.qm',  'Hachball',        'SR 1.7.2',  20, Duration.LOW,     Genre.SPORT_MANAGEMENT       ),  # noqa
(259, 'cze', 'Ikebana_cze.qm',   'Eeke-Baana',      'SR 1.7.2',  60, Duration.LOW,     Genre.LOGIC_PUZZLE           ),  # noqa
(260, 'en',  'Ikebana_eng.qm',   'Eeke-Baana',      'SR 1.7.2',  60, Duration.LOW,     Genre.LOGIC_PUZZLE           ),  # noqa
(261, 'fr',  'Ikebana_fra.qm',   'd\'Ike-baana',    'SR 1.7.2',  60, Duration.LOW,     Genre.LOGIC_PUZZLE           ),  # noqa
(262, 'hu',  'Ikebana_hun.qm',   'Eeke-Baana',      'SR 1.7.2',  60, Duration.LOW,     Genre.LOGIC_PUZZLE           ),  # noqa
(263, 'pl',  'Ikebana_pol.qm',   'Eeke-Baana',      'SR 1.7.2',  60, Duration.LOW,     Genre.LOGIC_PUZZLE           ),  # noqa
(264, 'cze', 'Murder_cze.qm',    'Vražda',          'SR 1.7.2',  75, Duration.AVERAGE, Genre.DETECTIVE              ),  # noqa
(265, 'en',  'Murder_eng.qm',    'Murder',          'SR 1.7.2',  75, Duration.AVERAGE, Genre.DETECTIVE              ),  # noqa
(266, 'fr',  'Murder_fra.qm',    'Meurtre',         'SR 1.7.2',  75, Duration.AVERAGE, Genre.DETECTIVE              ),  # noqa
(267, 'hu',  'Murder_hun.qm',    'Gyilkosság',      'SR 1.7.2',  75, Duration.AVERAGE, Genre.DETECTIVE              ),  # noqa
(268, 'pl',  'Murder_pol.qm',    'Morderstwo',      'SR 1.7.2',  75, Duration.AVERAGE, Genre.DETECTIVE              ),  # noqa
(269, 'cze', 'Prison1_cze.qm',   'Vězení',          'SR 1.7.2',  50, Duration.LONG,    Genre.PRISON_SIM             ),  # noqa
(270, 'en',  'Prison1_eng.qm',   'Prison',          'SR 1.7.2',  50, Duration.LONG,    Genre.PRISON_SIM             ),  # noqa
(271, 'fr',  'Prison1_fra.qm',   'Prison',          'SR 1.7.2',  50, Duration.LONG,    Genre.PRISON_SIM             ),  # noqa
(272, 'hu',  'Prison1_hun.qm',   'Börtön',          'SR 1.7.2',  50, Duration.LONG,    Genre.PRISON_SIM             ),  # noqa
(273, 'pl',  'Prison1_pol.qm',   'Więzienie',       'SR 1.7.2',  50, Duration.LONG,    Genre.PRISON_SIM             ),  # noqa
(274, 'cze', 'Tomb_cze.qm',      'Hrobka',          'SR 1.7.2',  20, Duration.LOW,     Genre.PUZZLE                 ),  # noqa
(275, 'en',  'Tomb_eng.qm',      'Tomb',            'SR 1.7.2',  20, Duration.LOW,     Genre.PUZZLE                 ),  # noqa
(276, 'fr',  'Tomb_fra.qm',      'Tombeau',         'SR 1.7.2',  20, Duration.LOW,     Genre.PUZZLE                 ),  # noqa
(277, 'hu',  'Tomb_hun.qm',      'Sír',             'SR 1.7.2',  20, Duration.LOW,     Genre.PUZZLE                 ),  # noqa
(278, 'pl',  'Tomb_pol.qm',      'Grób',            'SR 1.7.2',  20, Duration.LOW,     Genre.PUZZLE                 ),  # noqa
    # @formatter:on
]


# noinspection PyUnusedLocal
def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    Quest.insert_many(
        QUEST_NAMES,
        fields=[Quest.id, Quest.lang, Quest.file, Quest.name, Quest.gameVer,
                Quest.difficult, Quest.duration, Quest.genre]
    ).execute(database=database)


# noinspection PyUnusedLocal
def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    database.execute_sql('DELETE FROM quest WHERE id >= 209 AND id <= 278')
