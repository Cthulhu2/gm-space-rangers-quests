from contextlib import suppress

import peewee as pw
from peewee_migrate import Migrator

with suppress(ImportError):
    pass

# @formatter:off
QUEST_NAMES = [
    (  1, 'ru', 'Amnesia.qmm',             'Амнезия',                       'КР 2 Доминаторы',                          ),  # noqa
    (  2, 'ru', 'Badday.qmm',              'Плохой день рейнджера',         'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    (  3, 'en', 'Badday_eng.qm',           'Ranger\'s Bad Day',             'SR 2.1.2121 eng',                          ),  # noqa
    (  4, 'ru', 'Bank.qm',                 'Банк',                          'КР 1',                                     ),  # noqa
    (  5, 'ru', 'Banket.qmm',              'Банкет',                        'КР 2 Доминаторы',                          ),  # noqa
    (  6, 'en', 'Banket_eng.qm',           'Banquet',                       'SR 2.1.2121 eng',                          ),  # noqa
    (  7, 'ru', 'Boat.qm',                 'Лодка',                         'КР 1',                                     ),  # noqa
    (  8, 'ru', 'Bomber.qmm',              'Бомбер',                        'КР 2 Доминаторы',                          ),  # noqa
    (  9, 'ru', 'Bondiana.qm',             'Бондиана',                      'КР 1',                                     ),  # noqa
    ( 10, 'ru', 'Borzukhan.qmm',           'Борзухан',                      'КР 2 Доминаторы',                          ),  # noqa
    ( 11, 'en', 'Borzukhan_eng.qmm',       'Borzukhan',                     'SR 2.1.2121 eng',                          ),  # noqa
    ( 12, 'ru', 'Build.qm',                'Стройка',                       'КР 1',                                     ),  # noqa
    ( 13, 'ru', 'Casino.qm',               'Казино',                        'КР 1',                                     ),  # noqa
    ( 14, 'ru', 'Citadels.qmm',            'Цитадели',                      'КР 2 Доминаторы',                          ),  # noqa
    ( 15, 'ru', 'Codebox.qmm',             'Пятнашка',                      'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    ( 16, 'en', 'Codebox_eng.qm',          'Safecracking',                  'SR 2.1.2121 eng',                          ),  # noqa
    ( 17, 'ru', 'Colonization.qmm',        'Колонизация',                   'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    ( 18, 'ru', 'Commando.qm',             'Коммандо',                      'КР 1',                                     ),  # noqa
    ( 19, 'ru', 'Complex.qmm',             'Комплекс',                      'КР 2 Доминаторы HD Революция Фанатские',   ),  # noqa
    ( 20, 'ru', 'Cybersport.qmm',          'Киберспорт',                    'Фанатские',                                ),  # noqa
    ( 21, 'ru', 'Deadoralive.qmm',         'Живым или мёртвым',             'КР 2 Доминаторы HD Революция Оригинальные',),  # noqa
    ( 22, 'ru', 'Depth.qmm',               'Глубина',                       'КР 2 Доминаторы',                          ),  # noqa
    ( 23, 'en', 'Depth_eng.qm',            'Depth',                         'SR 2.1.2121 eng',                          ),  # noqa
    ( 24, 'ru', 'Diamond.qm',              'Бриллиант',                     'КР 1',                                     ),  # noqa
    ( 25, 'ru', 'Diehard.qm',              'Страшная смерть',               'КР 1',                                     ),  # noqa
    ( 26, 'ru', 'Disk.qmm',                'Диск',                          'КР 2 Доминаторы HD Революция Фанатские',   ),  # noqa
    ( 27, 'en', 'Disk_eng.qm',             'Disk',                          'SR 2.1.2121 eng',                          ),  # noqa
    ( 28, 'ru', 'Diver.qmm',               'Водолаз',                       'КР 2 Доминаторы',                          ),  # noqa
    ( 29, 'ru', 'Domoclan.qmm',            'Община свидетелей доминаторов', 'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    ( 30, 'ru', 'Doomino.qmm',             'Доомино',                       'КР 2 Доминаторы HD Революция Фанатские',   ),  # noqa
    ( 31, 'ru', 'Driver.qmm',              'Водитель',                      'КР 2 Доминаторы',                          ),  # noqa
    ( 32, 'en', 'Driver_eng.qm',           'Driver',                        'SR 2.1.2121 eng',                          ),  # noqa
    ( 33, 'ru', 'Drugs.qmm',               'Наркотики',                     'КР 2 Доминаторы',                          ),  # noqa
    ( 34, 'ru', 'Easywork.qmm',            'Лёгкая работа',                 'КР 2 Доминаторы',                          ),  # noqa
    ( 35, 'ru', 'Edelweiss.qmm',           'Эдельвейс',                     'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    ( 36, 'en', 'Edelweiss_eng.qm',        'Edelweiss',                     'SR 2.1.2121 eng',                          ),  # noqa
    ( 37, 'ru', 'Election.qmm',            'Выборы',                        'КР 2 Доминаторы',                          ),  # noqa
    ( 38, 'en', 'Election_eng.qm',         'Election',                      'SR 2.1.2121 eng',                          ),  # noqa
    ( 39, 'ru', 'Elus.qmm',                'Элус',                          'КР 2 Доминаторы',                          ),  # noqa
    ( 40, 'en', 'Elus_eng.qmm',            'Elus',                          'SR 2.1.2121 eng',                          ),  # noqa
    ( 41, 'ru', 'Energy.qm',               'Энергия',                       'КР 1',                                     ),  # noqa
    ( 42, 'ru', 'Evidence.qmm',            'Подстава',                      'КР 2 Доминаторы HD Революция Оригинальные',),  # noqa
    ( 43, 'en', 'Evidence_eng.qm',         'Frames',                        'SR 2.1.2121 eng',                          ),  # noqa
    ( 44, 'ru', 'Evilgenius.qmm',          'Злой гений',                    'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    ( 45, 'ru', 'Examen.qm',               'Экзамен',                       'КР 1',                                     ),  # noqa
    ( 46, 'ru', 'Faruk.qmm',               'Фарюки',                        'КР 2 Доминаторы',                          ),  # noqa
    ( 47, 'ru', 'Feipsycho.qmm',           'Фэянская психушка',             'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    ( 48, 'ru', 'Filial.qmm',              'Филиал',                        'КР 2 Доминаторы HD Революция Оригинальные',),  # noqa
    ( 49, 'ru', 'Fishing.qm',              'Рыбалка',                       'КР 1',                                     ),  # noqa
    ( 50, 'ru', 'Fishingcup.qmm',          'Чемпионат по рыбалке',          'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    ( 51, 'en', 'Fishingcup_eng.qm',       'Fishing Championship',          'SR 2.1.2121 eng',                          ),  # noqa
    ( 52, 'ru', 'Foncers.qmm',             'Фонсеры',                       'КР 2 Доминаторы',                          ),  # noqa
    ( 53, 'en', 'Foncers_eng.qm',          'Foncers',                       'SR 2.1.2121 eng',                          ),  # noqa
    ( 54, 'ru', 'Forum.qmm',               'Форум',                         'КР 2 Доминаторы HD Революция Оригинальные',),  # noqa
    ( 55, 'ru', 'Gaidnet.qmm',             'Гайд-нет',                      'КР 2 Доминаторы',                          ),  # noqa
    ( 56, 'ru', 'Galaxy.qm',               'Галактика',                     'КР 1',                                     ),  # noqa
    ( 57, 'ru', 'Gladiator.qm',            'Гладиатор',                     'КР 1',                                     ),  # noqa
    ( 58, 'ru', 'GLAVRED.qmm',             'Главный редактор',              'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    ( 59, 'ru', 'Gluki.qmm',               'Глюки',                         'КР 2 Доминаторы HD Революция Оригинальные',),  # noqa
    ( 60, 'ru', 'Gobsaur.qm',              'Гобзавр',                       'КР 1',                                     ),  # noqa
    ( 61, 'ru', 'Hachball.qm',             'Хэчбол',                        'КР 1',                                     ),  # noqa
    ( 62, 'ru', 'Ikebana.qm',              'Иикэ-Баана',                    'КР 1',                                     ),  # noqa
    ( 63, 'ru', 'Jumper.qmm',              'Джампер',                       'КР 2 Доминаторы',                          ),  # noqa
    ( 64, 'en', 'Jumper_eng.qm',           'Jumper',                        'SR 2.1.2121 eng',                          ),  # noqa
    ( 65, 'ru', 'Kiberrazum.qmm',          'Киберразум',                    'КР 2 Доминаторы HD Революция Фанатские',   ),  # noqa
    ( 66, 'ru', 'Kidnapped.qmm',           'Похищенный',                    'КР 2 2.1.2369',                            ),  # noqa
    ( 67, 'ru', 'Leonardo.qmm',            'Леонардо да Винчи',             'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    ( 68, 'en', 'Leonardo_eng.qm',         'Leonardo da Vinci',             'SR 2.1.2121 eng',                          ),  # noqa
    ( 69, 'ru', 'Logic.qmm',               'Логика',                        'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    ( 70, 'en', 'Logic_eng.qm',            'Logic',                         'SR 2.1.2121 eng',                          ),  # noqa
    ( 71, 'ru', 'LongLiveTheRanger.qmm',   'LongLiveTheRanger',             'Фанатские',                                ),  # noqa  # !!!
    ( 72, 'ru', 'Losthero.qmm',            'Потерянный герой',              'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    ( 73, 'ru', 'Mafia.qmm',               'Мафия',                         'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    ( 74, 'ru', 'mark05.qmm',              'mark05',                        'Фанатские',                                ),  # noqa  # !!!
    ( 75, 'ru', 'Massacri.qmm',            'Массакри',                      'Фанатские',                                ),  # noqa
    ( 76, 'ru', 'Maze.qmm',                'Лабиринт',                      'КР 2 Доминаторы',                          ),  # noqa
    ( 77, 'ru', 'Megatest.qmm',            'Мегатест',                      'КР 2 Доминаторы HD Революция Фанатские',   ),  # noqa
    ( 78, 'ru', 'Menzols.qm',              'Мензолы',                       'КР 1',                                     ),  # noqa
    ( 79, 'ru', 'Ministry.qmm',            'Министерство',                  'КР 2 Доминаторы',                          ),  # noqa
    ( 80, 'en', 'Ministry_eng.qm',         'Ministry',                      'SR 2.1.2121 eng',                          ),  # noqa
    ( 81, 'ru', 'Moi.qmm',                 'Мастер Иике-Бааны',             'КР 2 Доминаторы',                          ),  # noqa
    ( 82, 'ru', 'Murder.qm',               'Убийство',                      'КР 1',                                     ),  # noqa
    ( 83, 'ru', 'Muzon.qmm',               'Музон',                         'КР 2 Доминаторы',                          ),  # noqa
    ( 84, 'en', 'Muzon_eng.qm',            'Music Festival',                'SR 2.1.2121 eng',                          ),  # noqa
    ( 85, 'ru', 'Newflora.qm',             'Неофлора',                      'КР 1',                                     ),  # noqa
    ( 86, 'ru', 'Olympiada.qmm',           'Олимпиада (Клерки без границ)', 'КР 2 Доминаторы',                          ),  # noqa
    ( 87, 'en', 'Olympiada_eng.qm',        'Olympics (Clerks without End)', 'SR 2.1.2121 eng',                          ),  # noqa
    ( 88, 'ru', 'Pachvarash.qmm',          'Пачвараш',                      'КР 2 Доминаторы',                          ),  # noqa
    ( 89, 'en', 'Pachvarash_eng.qm',       'Pachvarash',                    'SR 2.1.2121 eng',                          ),  # noqa
    ( 90, 'ru', 'Park.qmm',                'Парк аттракционов',             'КР 2 Доминаторы',                          ),  # noqa
    ( 91, 'ru', 'Penetrator.qm',           'Пенетратор',                    'КР 1',                                     ),  # noqa
    ( 92, 'ru', 'Pharaon.qmm',             'Фараон',                        'КР 2 Доминаторы',                          ),  # noqa
    ( 93, 'ru', 'Photorobot.qmm',          'Фоторобот',                     'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    ( 94, 'ru', 'Pilot.qmm',               'Пилот',                         'КР 2 Доминаторы',                          ),  # noqa
    ( 95, 'en', 'Pilot_eng.qm',            'Pilot',                         'SR 2.1.2121 eng',                          ),  # noqa
    ( 96, 'ru', 'PirateClanPrison.qmm',    'Тюрьма (пиратская)',            'SR 2.1.2170',                              ),  # noqa
    ( 97, 'en', 'PirateClanPrison_eng.qm', 'Prison (pirate)',               'SR 2.1.2121 eng',                          ),  # noqa
    ( 98, 'ru', 'Piratesnest.qmm',         'Гнездо пиратов',                'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    ( 99, 'ru', 'Pizza.qmm',               'Пицца',                         'КР 2 Доминаторы',                          ),  # noqa
    (100, 'en', 'Pizza_eng.qm',            'Pizza',                         'SR 2.1.2121 eng',                          ),  # noqa
    (101, 'ru', 'Player.qmm',              'Проигрыватель',                 'КР 2 Доминаторы',                          ),  # noqa
    (102, 'en', 'Player_eng.qm',           'Player',                        'SR 2.1.2121 eng',                          ),  # noqa
    (103, 'ru', 'Poroda.qm',               'Порода',                        'КР 1',                                     ),  # noqa
    (104, 'ru', 'Prison.qmm',              'Тюрьма',                        'КР 2 Доминаторы',                          ),  # noqa
    (105, 'ru', 'Prison1.qm',              'Тюрьма (КР1)',                  'КР 1',                                     ),  # noqa
    (106, 'en', 'Prison_eng.qm',           'Prison',                        'SR 2.1.2121 eng',                          ),  # noqa
    (107, 'ru', 'Proprolog.qmm',           'Пропролог',                     'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    (108, 'ru', 'Provoda.qmm',             'Провода',                       'КР 2 Доминаторы HD Революция Оригинальные',),  # noqa
    (109, 'ru', 'Rally.qmm',               'Ралли',                         'КР 2 Доминаторы HD Революция Фанатские',   ),  # noqa
    (110, 'en', 'Rally_eng.qm',            'Rally',                         'SR 2.1.2121 eng',                          ),  # noqa
    (111, 'ru', 'Robots.qmm',              'Роботы',                        'КР 2 Доминаторы',                          ),  # noqa
    (112, 'en', 'Robots_eng.qm',           'Robots',                        'SR 2.1.2121 eng',                          ),  # noqa
    (113, 'ru', 'Rush.qm',                 'Гонка',                         'КР 1',                                     ),  # noqa
    (114, 'ru', 'Rvk.qmm',                 'Военкомат',                     'КР 2 Доминаторы',                          ),  # noqa
    (115, 'ru', 'Shashki.qmm',             'Плазмошашки',                   'КР 2 Доминаторы',                          ),  # noqa
    (116, 'en', 'Shashki_eng.qm',          'Plasmo-checkers',               'SR 2.1.2121 eng',                          ),  # noqa
    (117, 'ru', 'Sibolusovt.qmm',          'Ухоногий сиболусовт',           'КР 2 Доминаторы HD Революция Фанатские',   ),  # noqa
    (118, 'en', 'Sibolusovt_eng.qm',       'Sibolusovtus',                  'SR 2.1.2121 eng',                          ),  # noqa
    (119, 'ru', 'Siege.qmm',               'Осада',                         'КР 1',                                     ),  # noqa
    (120, 'ru', 'Ski.qmm',                 'Лыжный курорт',                 'КР 2 Доминаторы',                          ),  # noqa
    (121, 'en', 'Ski_eng.qm',              'Ski Resort',                    'SR 2.1.2121 eng',                          ),  # noqa
    (122, 'ru', 'Sortirovka1.qmm',         'Сортировка',                    'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    (123, 'en', 'Sortirovka1_eng.qm',      'Sorting',                       'SR 2.1.2121 eng',                          ),  # noqa
    (124, 'ru', 'SpaceLines.qmm',          'Космолинии',                    'КР 2 Доминаторы HD Революция Фанатские',   ),  # noqa
    (125, 'en', 'SpaceLines_eng.qm',       'Cosmic Lines',                  'SR 2.1.2121 eng',                          ),  # noqa
    (126, 'ru', 'Spy.qm',                  'Шпион',                         'КР 1',                                     ),  # noqa
    (127, 'ru', 'Stealth.qmm',             'Стелс',                         'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    (128, 'en', 'Stealth_eng.qm',          'Stealth Ship',                  'SR 2.1.2121 eng',                          ),  # noqa
    (129, 'ru', 'Svarokok.qmm',            'Сварокок',                      'КР 2 Доминаторы',                          ),  # noqa
    (130, 'en', 'Svarokok_eng.qm',         'Swarokok',                      'SR 2.1.2121 eng',                          ),  # noqa
    (131, 'ru', 'Taxist.qmm',              'Таксист',                       'КР 2 Доминаторы HD Революция Фанатские',   ),  # noqa
    (132, 'ru', 'Testing.qmm',             'Тестинг',                       'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    (133, 'ru', 'Tomb.qm',                 'Гробница',                      'КР 1',                                     ),  # noqa
    (134, 'ru', 'Tourists.qmm',            'Туристы',                       'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    (135, 'ru', 'Vulkan.qmm',              'Вулканический остров',          'КР 2 Доминаторы Перезагрузка',             ),  # noqa
    (136, 'ru', 'Xenolog.qmm',             'Ксенолог',                      'КР 2 Доминаторы',                          ),  # noqa
    (137, 'ru', 'Xenopark.qmm',            'Ксенопарк',                     'КР 2 Доминаторы',                          ),  # noqa
    (138, 'en', 'Xenopark_eng.qm',         'Xenopark',                      'SR 2.1.2121 eng',                          ),  # noqa
]
# @formatter:on


class Quest(pw.Model):
    id = pw.IntegerField(primary_key=True)
    name = pw.CharField(max_length=128)
    file = pw.CharField(max_length=128)
    lang = pw.CharField(max_length=5)
    gameVer = pw.CharField(max_length=128)

    class Meta:
        table_name = 'quest'


# noinspection PyUnusedLocal
def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    Quest.insert_many(
        QUEST_NAMES,
        fields=[Quest.id, Quest.lang, Quest.file, Quest.name, Quest.gameVer]
    ).execute(database=database)


# noinspection PyUnusedLocal
def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    database.execute_sql('DELETE FROM quest WHERE id >= 1 AND id <= 138')
