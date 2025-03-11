from enum import IntEnum, auto

import peewee as pw
from peewee_migrate import Migrator


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
    LOW = 1            # низкая
    BELOW_AVERAGE = 2  # ниже средней
    AVERAGE = 3        # средняя
    ABOVE_AVERAGE = 4  # выше средней
    LONG = 5           # высокая


# noinspection PyUnusedLocal
def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.add_fields('options',
                        sort_dir=pw.SmallIntegerField(default=1),
                        sort_type=pw.SmallIntegerField(default=1))

    migrator.add_fields('quest',
                        difficult=pw.SmallIntegerField(null=True),
                        genre=pw.SmallIntegerField(null=True),
                        duration=pw.SmallIntegerField(null=True))

    for file, diff, duration, genre in (
            # @formatter:off
# SR 1
('Bank',       88, Duration.AVERAGE, Genre.ESPIONAGE),                         # noqa  88 (fandom,  88 Средняя)
('Boat',       15, Duration.LOW,     Genre.PUZZLE),                            # noqa  15 (fandom,  15 Низкая )
('Bondiana',   50, Duration.LOW,     Genre.ADVENTURE_SHOOTER),                 # noqa  50 (fandom,  50 Низкая )
('Build',      50, Duration.LOW,     Genre.BUILD_MANAGEMENT),                  # noqa  50 (fandom,  50 Низкая )
('Casino',     50, Duration.LONG,    Genre.GAMBLING),                          # noqa  50 (fandom,  50 Высокая)
('Commando',   50, Duration.AVERAGE, Genre.ASSAULT),                           # noqa  50 (fandom,  50 Средняя)
('Diamond',    50, Duration.AVERAGE, Genre.ADVENTURE_SHOOTER_SAFE_CRACK_SIM),  # noqa  50 (fandom,  50 Средняя)
('Diehard',    10, Duration.LOW,     Genre.LAB_RAT_SIM),                       # noqa  10 (fandom,  10 Низкая )
('Energy',     73, Duration.AVERAGE, Genre.LOGIC_PUZZLE),                      # noqa  73 (fandom,  73 Средняя)
('Examen',     50, Duration.LOW,     Genre.PASSING_ENTRANCE_EXAMS),            # noqa  50 (fandom,  50 Низкая )
# before Fishingcup, because of LIKE%
('Fishing',    50, Duration.LOW,     Genre.FISHING_SIM),                       # noqa  50 (fandom,  50 Низкая )
('Galaxy',     85, Duration.AVERAGE, Genre.ESPIONAGE_GAMBLING),                # noqa  85 (fandom,  85 Средняя)
('Gladiator', 100, Duration.LOW,     Genre.MANAGEMENT),                        # noqa  50 (fandom, 100 Низкая )
('Gobsaur',    10, Duration.LOW,     Genre.WILD_GOBZAUR_TAMING_SIM),           # noqa  10 (fandom,  10 Низкая )
('Hachball',   20, Duration.LOW,     Genre.SPORT_MANAGEMENT),                  # noqa  20 (fandom,  20 Низкая )
('Ikebana',    60, Duration.LOW,     Genre.LOGIC_PUZZLE),                      # noqa  60 (fandom,  60 Низкая )
('Menzols',    50, Duration.AVERAGE, Genre.TRADING),                           # noqa  50 (fandom,  50 Средняя)
('Murder',     75, Duration.AVERAGE, Genre.DETECTIVE),                         # noqa  75 (fandom,  75 Средняя)
('Newflora',   50, Duration.AVERAGE, Genre.ESPIONAGE),                         # noqa  50 (fandom,  50 Средняя)
('Penetrator', 50, Duration.LOW,     Genre.WEAPONS_TESTING),                   # noqa  50 (fandom,  50 Низкая )
('Poroda',    100, Duration.LOW,     Genre.PENCHEKRACK_BREEDING_SIM),          # noqa 100 (fandom, 100 Низкая )
('Rush',       30, Duration.LONG,    Genre.ANCIENT_CARS_RACING_SIM),           # noqa  30 (fandom,  30 Высокая)
('Siege',      50, Duration.LONG,    Genre.FORTRESS_DEFEND),                   # noqa  50 (fandom,  50 Высокая)
('Spy',        28, Duration.AVERAGE, Genre.ESPIONAGE_BUGGING),                 # noqa  28 (fandom,  28 Средняя)
('Tomb',       20, Duration.LOW,     Genre.PUZZLE),                            # noqa  20 (fandom,  20 Низкая )
# SR 2
('Amnesia',      70, Duration.LOW,           Genre.ADVENTURE_SHOOTER),                 # noqa 70  (res, 40 3) (help, выше средней выше средней) (fanodm, 70  Низкая       )
('Banket',       70, Duration.AVERAGE,       Genre.LOGIC_EDUCATIONAL_GAME),            # noqa 70  (res, 23 2) (help, средняя      средняя     ) (fandom, 70  Средняя      )
('Badday',       50, Duration.AVERAGE,       Genre.ADVENTURE_W_FIGHTING_ELEMENTS),     # noqa 50  (res, 25 2) (help, средняя      средняя     ) (fandom, 50  Средняя      )
('Bomber',       70, Duration.AVERAGE,       Genre.LOGIC_TACTICAL_GAME),               # noqa 70  (res, 24 2) (help, средняя      средняя     ) (fandom, 70  Средняя      )
('Borzukhan',    30, Duration.BELOW_AVERAGE, Genre.ADVENTURE_W_ARCADE_ELEMENTS),       # noqa 30  (res,  7 3) (help, ниже средней ниже средней) (fandom, 30  Ниже средней )
('Citadels',     50, Duration.AVERAGE,       Genre.TACTICAL_STRATEGY),                 # noqa 50  (res, 29 2) (help, средняя      средняя     ) (fandom, 50  Средняя      )
('Codebox',      65, Duration.LOW,           Genre.LOGIC_PUZZLE),                      # noqa 65  (res, 36 3) (help, выше средней выше средней) (fandom, 65  Низкая       )
('Colonization', 75, Duration.LONG,          Genre.ECONOMY_SIM),                       # noqa 75  (res, 42 4) (help, выше средней высокая     ) (fandom, 75  Высокая      )
('Complex',      50, Duration.LONG,          Genre.DETECTIVE),                         # noqa 65  (res, 56 4) (help, выше средней высокая     ) (fandom, 50  Высокая      )
('Deadoralive',  50, Duration.AVERAGE,       Genre.ADVENTURE_W_ADVENTURES),            # noqa 50  (res, 53 3) (help, выше средней выше средней) (fandom, 50  Средняя      )
('Depth',        90, Duration.LONG,          Genre.LOGIC_MATH_GAME),                   # noqa 90  (res, 48 4) (help, высокая      высокая     ) (fandom, 90  Высокая      )
('Disk',         20, Duration.AVERAGE,       Genre.CARGO_DELIVERY_W_QUEST_ELEMENTS),   # noqa 50  (res, 17 0) (help, средняя      низкая      ) (fandom, 20  Средняя      )
('Diver',        90, Duration.LOW,           Genre.ADVENTURE),                         # noqa 90  (res, 16 0) (help, средняя      низкая      ) (fandom, 90  Низкая       )
('Domoclan',     80, Duration.LONG,          Genre.ADVENTURE_W_ADVENTURES),            # noqa 80  (res, 49 4) (help, высокая      высокая     ) (fandom, 80  Высокая      )
('Doomino',      50, Duration.AVERAGE,       Genre.LOGIC_GAME),                        # noqa 50  (res, 21 2) (help, средняя      средняя     ) (fandom, 50  Средняя      )
('Driver',       50, Duration.LONG,          Genre.HAULER_SIM),                        # noqa 50  (res, 32 3) (help, средняя      выше средней) (fandom, 50  Выше средней*)
('Drugs',        80, Duration.LOW,           Genre.ADVENTURE_W_LOGIC_PUZZLES),         # noqa 80  (res, 52 4) (help, высокая      высокая     ) (fandom, 80  Высокая     *)
('Easywork',    100, Duration.LONG,          Genre.LOGIC_PUZZLES_AND_MATH_PROBLEMS),   # noqa 100 (res, 50 4) (help, высокая      высокая     ) (fandom, 100 Высокая      )
('Edelweiss',    75, Duration.AVERAGE,       Genre.ADVENTURE_W_ADVENTURES),            # noqa 35  (res,  8 2) (help, ниже средней средняя     ) (fandom, 75  Средняя      )
('Election',     30, Duration.LOW,           Genre.ELECTION_CAMPAIGN_SIM),             # noqa 30  (res,  2 0) (help, низкая       низкая      ) (fandom, 30  Низкая       )
('Elus',         60, Duration.LOW,           Genre.LOGIC_PUZZLE),                      # noqa 60  (res, 44 2) (help, высокая      средняя     ) (fandom, 60  Низкая       )
('Evidence',     50, Duration.AVERAGE,       Genre.HUMOROUS_DETECTIVE),                # noqa 50  (res, 37 2) (help, средняя      средняя     ) (fandom, 50  Средняя      )
('Evilgenius',   50, Duration.LONG,          Genre.STRATEGY_W_FIGHTING_ELEMENTS),      # noqa 65  (res, 38 4) (help, выше средней высокая     ) (fandom, 50  Высокая      )
('Faruk',        70, Duration.AVERAGE,       Genre.MATH_LOGIC_PUZZLE),                 # noqa 70  (res, 35 2) (help, выше средней средняя     ) (fandom, 70  Средняя      )
('Feipsycho',    50, Duration.BELOW_AVERAGE, Genre.ADVENTURE_W_LOGIC_PUZZLES),         # noqa 50  (res, 21 1) (help, средняя      ниже средней) (fandom, 50  Ниже средней )
('Filial',       50, Duration.AVERAGE,       Genre.ADVENTURE_W_ADVENTURES),            # noqa 50  (res, 46 3) (help, выше средней выше средней) (fandom, 50  Средняя      )
('Fishingcup',   45, Duration.AVERAGE,       Genre.FISHING_SIM),                       # noqa 45  (res, 12 2) (help, ниже средней средняя     ) (fandom, 45  Cредняя      )
('Foncers',      40, Duration.AVERAGE,       Genre.RACING_SIM),                        # noqa 40  (res,  9 2) (help, ниже средней средняя     ) (fandom, 40  Средняя      )
('Forum',        75, Duration.LONG,          Genre.ADVENTURE_W_ADVENTURES),            # noqa 75  (res, 29 2) (help, средняя      средняя     ) (fandom, 75  Высокая      )
('GLAVRED',      25, Duration.LONG,          Genre.ECONOMY_SIM),                       # noqa 25  (res, 45 3) (help, высокая      высокая     ) (fandom, 25  Высокая      )
('Gaidnet',     100, Duration.LONG,          Genre.LOGIC_PUZZLE),                      # noqa 100 (res, 53 4) (help, высокая      высокая     ) (fandom, 100 Высокая      )
('Gluki',        50, Duration.BELOW_AVERAGE, Genre.ADVENTURE_W_AWFUL_HORROR_ELEMENTS), # noqa 50  (res, 28 2) (help, средняя      средняя     ) (fandom, 50  Ниже средней )
('Jumper',       80, Duration.AVERAGE,       Genre.LOGIC_PUZZLE),                      # noqa 80  (res, 46 2) (help, высокая      средняя     ) (fandom, 80  Средняя      )
('Kiberrazum',   50, Duration.LONG,          Genre.ADVENTURE_W_HORROR_ELEMENTS),       # noqa 50  (res, 55 4) (help, выше средней высокая     ) (fandom, 50  Высокая      )
('Kidnapped',    75, Duration.LONG,          Genre.ADVENTURE_W_ADVENTURES),            # noqa 0   (res, 53 3) (help,                          ) (fandom, 75  Высокая      )
('Leonardo',     70, Duration.AVERAGE,       Genre.LOGIC_EASEL_SIMULATOR),             # noqa 70  (res, 33 2) (help, выше средней средняя     ) (fandom, 70  Средняя      )
('Logic',        30, Duration.LOW,           Genre.LOGIC_PUZZLE),                      # noqa 30  (res,  6 0) (help, ниже средней низкая      ) (fandom, 30  Низкая       )
('Losthero',     55, Duration.AVERAGE,       Genre.ADVENTURE_W_ADVENTURES),            # noqa 55  (res, 31 3) (help, выше средней средняя     ) (fandom, 55  Средняя      )
('Mafia',        85, Duration.LONG,          Genre.ADVENTURE_W_ADVENTURES),            # noqa 85  (res, 54 4) (help, высокая      высокая     ) (fandom, 85  Высокая      )
('Maze',        100, Duration.LONG,          Genre.ADVENTURE_W_LOGIC_PUZZLES),         # noqa 100 (res, 51 4) (help, высокая      высокая     ) (fandom, 100 Высокая      )
('Megatest',     50, Duration.LOW,           Genre.TRIVIA_GAME),                       # noqa 50  (res,  6 2) (help, ниже средней ниже средней) (fandom, 50  Низкая       )
('Ministry',     20, Duration.AVERAGE,       Genre.ADVENTURE_W_LOGIC_ELEMENTS),        # noqa 20  (res,  3 2) (help, низкая       средняя     ) (fandom, 20  Средняя      )
('Moi',          70, Duration.LONG,          Genre.FANTASY_ROLE_PLAYING_GAME),         # noqa 70  (res, 55 4) (help, высокая      высокая     ) (fandom, 70  Высокая      )
('Muzon',        20, Duration.AVERAGE,       Genre.ADVENTURE_W_MANAGEMENT_ELEMENTS),   # noqa 20  (res,  5 2) (help, низкая       средняя     ) (fandom, 20  Средняя      )
('Olympiada',    60, Duration.LONG,          Genre.LOGIC_GAME_W_MANAGEMENT_ELEMENTS),  # noqa 60  (res, 47 4) (help, высокая      высокая     ) (fandom, 60  Высокая      )
('Pachvarash',   50, Duration.ABOVE_AVERAGE, Genre.ANIMAL_LIFE_SIM),                   # noqa 50  (res, 37 3) (help, выше средней выше средней) (fandom, 50  Выше средней )
('Park',         70, Duration.ABOVE_AVERAGE, Genre.ADVENTURE_W_LOGIC_PUZZLES),         # noqa 70  (res, 34 3) (help, выше средней выше средней) (fandom, 70  Выше средней )
('Pharaon',      20, Duration.LOW,           Genre.TEXT_AND_LOGIC_PUZZLE),             # noqa 20  (res,  1 0) (help, низкая       низкая      ) (fandom, 20  Низкая       )
('Photorobot',   50, Duration.BELOW_AVERAGE, Genre.LOGIC_MATH_GAME),                   # noqa 50  (res, 20 1) (help, средняя      ниже средней) (fandom, 50  Ниже средней )
('Pilot',        30, Duration.AVERAGE,       Genre.ADVENTURE_W_LOGIC_PUZZLES),         # noqa 30  (res,  4 2) (help, низкая       средняя     ) (fandom, 30  Средняя      )
('PirateClanPrison', 50, Duration.LONG,      Genre.PRISON_SIM),                        # noqa 50  (res,  0 2) (help,                          ) (fandom,                  )
('Prison',       50, Duration.LONG,          Genre.PRISON_SIM),                        # noqa 50  (res,  0 2) (help,                          ) (fandom, 50  Высокая      )
('Piratesnest',  70, Duration.ABOVE_AVERAGE, Genre.ADVENTURE_W_LOGIC_PUZZLES),         # noqa 70  (res, 39 3) (help, выше средней выше средней) (fandom, 70  Выше средней )
('Pizza',        22, Duration.AVERAGE,       Genre.LOGIC_MATH_GAME),                   # noqa 50  (res, 22 2) (help, средняя      средняя     ) (fandom, 50  Средняя      )
('Player',       20, Duration.LOW,           Genre.LOGIC_GAME),                        # noqa 20  (res, 15 0) (help, средняя      низкая      ) (fandom, 20  Низкая       )
('Proprolog',    85, Duration.AVERAGE,       Genre.SPACE_RANGERS_SIM),                 # noqa 85  (res, 43 3) (help, высокая      выше средней) (fandom, 85  Средняя      )
('Provoda',      50, Duration.AVERAGE,       Genre.LOGIC_MATH_GAME),                   # noqa 50  (res, 32 2) (help, средняя      ниже средней) (fandom, 50  Низкая      *)
('Rally',        50, Duration.AVERAGE,  Genre.RACING_SIM_W_MANAGEMENT_ELEMENTS),       # noqa 50  (res, 48 2) (help, выше средней средняя     ) (fandom, 50  Средняя      )
('Robots',       50, Duration.AVERAGE,       Genre.TACTICAL_FIGHTING),                 # noqa 30  (res, 14 2) (help, ниже средней средняя     ) (fandom, 50  Средняя      )
('Rvk',          30, Duration.AVERAGE,       Genre.RECRUITMENT_CENTER_MANAGER),        # noqa 30  (res, 27 2) (help, средняя      средняя     ) (fandom, 30  Средняя      )
('Shashki',      30, Duration.LOW,           Genre.MATH_PUZZLE),                       # noqa 30  (res, 18 1) (help, средняя      низкая      ) (fandom, 30  Низкая       )
('Sibolusovt',   50, Duration.AVERAGE,       Genre.ADVENTURE_W_BLACK_HUMOR_ELEMENTS),  # noqa 50  (res, 70 4) (help, высокая      высокая     ) (fandom, 50  Средняя      )
('Ski',          40, Duration.AVERAGE,       Genre.ECONOMY_SIM),                       # noqa 40  (res, 13 2) (help, ниже средней средняя     ) (fandom, 40  Средняя      )
('Sortirovka1',  40, Duration.AVERAGE,       Genre.ARCADE_LOGIC_GAME),                 # noqa 40  (res, 10 2) (help, ниже средней средняя     ) (fandom, 40  Средняя      )
('SpaceLines',   50, Duration.ABOVE_AVERAGE, Genre.ECONOMIC_STRATEGY),                 # noqa 50  (res, 30 3) (help, средняя      выше средней) (fandom, 50  Средняя      )
('Stealth',      35, Duration.BELOW_AVERAGE, Genre.ADVENTURE_SHOOTER),                 # noqa 50  (res, 19 1) (help, средняя      ниже средней) (fandom, 35  Ниже средней )
('Svarokok',     40, Duration.AVERAGE,       Genre.TACTICAL_GAME),                     # noqa 40  (res, 11 2) (help, ниже средней средняя     ) (fandom, 40  Средняя      )
('Taxist',       40, Duration.AVERAGE,       Genre.TAXI_SIM),                          # noqa 40  (res, 31 2) (help, средняя      средняя     ) (fandom, 40  Средняя      )
('Testing',      75, Duration.LONG,          Genre.ADVENTURE_W_FIGHTING_N_PUZZLE_ELEMENTS), # noqa 75 (res, 41 4) (help, выше средней высокая ) (fandom, 75  Высокая      )
('Tourists',     50, Duration.AVERAGE,       Genre.ADVENTURE_W_LOGIC_PUZZLES),         # noqa 50  (res, 26 2) (help, средняя      средняя     ) (fandom, 50  Средняя      )
('Vulkan',       50, Duration.AVERAGE,       Genre.ADVENTURE_W_ADVENTURES),            # noqa 50  (res, 30 2) (help,                          ) (fandom, 50  Средняя      )
('Xenolog',      50, Duration.AVERAGE,       Genre.ADVENTURE),                         # noqa 50  (res, 28 2) (help, средняя      средняя     ) (fandom, 50  Средняя      )
('Xenopark',     60, Duration.LOW,           Genre.LOGIC_PUZZLE),                      # noqa 60  (res, 17 0) (help, средняя      низкая      ) (fandom, 60  Низкая       )
# Fans
('Cybersport',        50, Duration.LONG, Genre.SIMULATOR),  # noqa 50 (fandom, 50 Высокая)
# ('LongLiveTheRanger', 100, Duration.LOW, Genre.LOGIC_MATH_GAME),  # noqa 0 (fandom, )
# ('mark05',            40, Duration.LOW, Genre.LOGIC_MATH_GAME),  # noqa 0 (fandom, )
('Massacri',          38, Duration.LONG, Genre.ACTION_HORROR),  # noqa 0 (fandom, 38 Высокая)
            # @formatter:on
    ):
        migrator.sql(
            f'UPDATE quest SET'
            f'  difficult = {diff},'
            f'  duration = {duration},'
            f'  genre = {genre} '
            f"WHERE quest.file LIKE '{file}%'")


# noinspection PyUnusedLocal
def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.remove_fields('quest', 'difficult', 'genre', 'duration')
    migrator.remove_fields('options', 'sort_dir', 'sort_type')
