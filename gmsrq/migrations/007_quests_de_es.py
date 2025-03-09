from contextlib import suppress

import peewee as pw
from peewee_migrate import Migrator

with suppress(ImportError):
    pass

# @formatter:off
QUEST_NAMES = [
    (139, 'de', 'Badday_ger.qmm',           'Ein schelchter tag',           'SR 2.1.2468 ger',),  # noqa
    (140, 'es', 'Badday_spa.qmm',           'Mal Día de Ranger',            'SR 2.1.2468 spa',),  # noqa
    (141, 'de', 'Banket_ger.qmm',           'Bankett',                      'SR 2.1.2468 ger',),  # noqa
    (142, 'es', 'Banket_spa.qmm',           'Banquete',                     'SR 2.1.2468 spa',),  # noqa
    (143, 'de', 'Borzukhan_ger.qmm',        'Borzukhan',                    'SR 2.1.2468 ger',),  # noqa
    (144, 'es', 'Borzukhan_spa.qmm',        'Borzukhan',                    'SR 2.1.2468 spa',),  # noqa
    (145, 'de', 'Codebox_ger.qmm',          'Krönung des Maloqarchen',      'SR 2.1.2468 ger',),  # noqa
    (146, 'es', 'Codebox_spa.qmm',          'Etiqueta',                     'SR 2.1.2468 spa',),  # noqa
    (147, 'de', 'Depth_ger.qmm',            'Tiefe',                        'SR 2.1.2468 ger',),  # noqa
    (148, 'es', 'Depth_spa.qmm',            'Profundidad',                  'SR 2.1.2468 spa',),  # noqa
    (149, 'de', 'Disk_ger.qmm',             'Disk',                         'SR 2.1.2468 ger',),  # noqa
    (150, 'es', 'Disk_spa.qmm',             'Disco',                        'SR 2.1.2468 spa',),  # noqa
    (151, 'de', 'Driver.qmm',               'Fahrer',                       'SR 2.1.2468 ger',),  # noqa
    (152, 'es', 'Driver_spa.qmm',           'Conductor',                    'SR 2.1.2468 spa',),  # noqa
    (153, 'de', 'Edelweiss_ger.qmm',        'Edelweiß',                     'SR 2.1.2468 ger',),  # noqa
    (154, 'es', 'Edelweiss_spa.qmm',        'Edelweiss',                    'SR 2.1.2468 spa',),  # noqa
    (155, 'de', 'Election_ger.qmm',         'Wahlen',                       'SR 2.1.2468 ger',),  # noqa
    (156, 'es', 'Election_spa.qmm',         'Elección',                     'SR 2.1.2468 spa',),  # noqa
    (157, 'de', 'Elus_ger.qmm',             'Eloose',                       'SR 2.1.2468 ger',),  # noqa
    (158, 'es', 'Elus_spa.qmm',             'Eloose',                       'SR 2.1.2468 spa',),  # noqa
    (159, 'de', 'Evidence_ger.qmm',         'Beweis',                       'SR 2.1.2468 ger',),  # noqa
    (160, 'es', 'Evidence_spa.qmm',         'Cuadro',                       'SR 2.1.2468 spa',),  # noqa
    (161, 'de', 'Fishingcup_ger.qmm',       'Angelmeisterschaft',           'SR 2.1.2468 ger',),  # noqa
    (162, 'es', 'Fishingcup_spa.qmm',       'Campeonato de Pesca',          'SR 2.1.2468 spa',),  # noqa
    (163, 'de', 'Foncers_ger.qmm',          'Foncerrennen',                 'SR 2.1.2468 ger',),  # noqa
    (164, 'es', 'Foncers_spa.qmm',          'Fonsers',                      'SR 2.1.2468 spa',),  # noqa
    (165, 'de', 'Jumper_ger.qmm',           'Springer',                     'SR 2.1.2468 ger',),  # noqa
    (166, 'es', 'Jumper_spa.qmm',           'Saltador',                     'SR 2.1.2468 spa',),  # noqa
    (167, 'de', 'Leonardo_ger.qmm',         'Leonardo da Vinci',            'SR 2.1.2468 ger',),  # noqa
    (168, 'es', 'Leonardo_spa.qmm',         'Leonardo da Vinci',            'SR 2.1.2468 spa',),  # noqa
    (169, 'de', 'Logic_ger.qmm',            'Maloq Logik',                  'SR 2.1.2468 ger',),  # noqa
    (170, 'es', 'Logic_spa.qmm',            'Lógica',                       'SR 2.1.2468 spa',),  # noqa
    (171, 'de', 'Ministry_ger.qmm',         'Ministerium',                  'SR 2.1.2468 ger',),  # noqa
    (172, 'es', 'Ministry_spa.qmm',         'Ministerio',                   'SR 2.1.2468 spa',),  # noqa
    (173, 'de', 'Muzon_ger.qmm',            'Musikfestival',                'SR 2.1.2468 ger',),  # noqa
    (174, 'es', 'Muzon_spa.qmm',            'Festival de Música',           'SR 2.1.2468 spa',),  # noqa
    (175, 'de', 'Olympiada_ger.qmm',        'Olympia',                      'SR 2.1.2468 ger',),  # noqa
    (176, 'es', 'Olympiada_spa.qmm',        'Juegos Olímpicos',             'SR 2.1.2468 spa',),  # noqa
    (177, 'de', 'Pachvarash_ger.qmm',       'Pachvaraus',                   'SR 2.1.2468 ger',),  # noqa
    (178, 'es', 'Pachvarash_spa.qmm',       'Pachvaraus',                   'SR 2.1.2468 spa',),  # noqa
    (179, 'de', 'Pilot_ger.qmm',            'Pilot',                        'SR 2.1.2468 ger',),  # noqa
    (180, 'es', 'Pilot_spa.qmm',            'Piloto',                       'SR 2.1.2468 spa',),  # noqa
    (181, 'de', 'PirateClanPrison_ger.qmm', 'Gefängnis (pirat)',            'SR 2.1.2468 ger',),  # noqa
    (182, 'es', 'PirateClanPrison_spa.qmm', 'Prisión (pirata)',             'SR 2.1.2468 spa',),  # noqa
    (183, 'de', 'Pizza_ger.qmm',            'Pizza',                        'SR 2.1.2468 ger',),  # noqa
    (184, 'es', 'Pizza_spa.qmm',            'Pizza',                        'SR 2.1.2468 spa',),  # noqa
    (185, 'de', 'Player_ger.qmm',           'Abspielgerät',                 'SR 2.1.2468 ger',),  # noqa
    (186, 'es', 'Player_spa.qmm',           'Tocadiscos',                   'SR 2.1.2468 spa',),  # noqa
    (187, 'de', 'Prison_ger.qmm',           'Gefängnis',                    'SR 2.1.2468 ger',),  # noqa
    (188, 'es', 'Prison_spa.qmm',           'Prisión',                      'SR 2.1.2468 spa',),  # noqa
    (189, 'de', 'Rally_ger.qmm',            'Rallye',                       'SR 2.1.2468 ger',),  # noqa
    (190, 'es', 'Rally_spa.qmm',            'Rally',                        'SR 2.1.2468 spa',),  # noqa
    (191, 'de', 'Robots_ger.qmm',           'Mini-Roboterschlachten',       'SR 2.1.2468 ger',),  # noqa
    (192, 'es', 'Robots_spa.qmm',           'Batallas de Minirobots',       'SR 2.1.2468 spa',),  # noqa
    (193, 'de', 'Shashki_ger.qmm',          'Dame',                         'SR 2.1.2468 ger',),  # noqa
    (194, 'es', 'Shashki_spa.qmm',          'Dames',                        'SR 2.1.2468 spa',),  # noqa
    (195, 'de', 'Sibolusovt_ger.qmm',       'Auropedal Sibolusovtus',       'SR 2.1.2468 ger',),  # noqa
    (196, 'es', 'Sibolusovt_spa.qmm',       'Sibolusovtus Auropedal',       'SR 2.1.2468 spa',),  # noqa
    (197, 'de', 'Ski_ger.qmm',              'Ski Resort',                   'SR 2.1.2468 ger',),  # noqa
    (198, 'es', 'Ski_spa.qmm',              'Estación de Esquí',            'SR 2.1.2468 spa',),  # noqa
    (199, 'de', 'Sortirovka1_ger.qmm',      'Sortierer',                    'SR 2.1.2468 ger',),  # noqa
    (200, 'es', 'Sortirovka1_spa.qmm',      'Surtido',                      'SR 2.1.2468 spa',),  # noqa
    (201, 'de', 'SpaceLines_ger.qmm',       'Passagiertransport RaumLiner', 'SR 2.1.2468 ger',),  # noqa
    (202, 'es', 'SpaceLines_spa.qmm',       'Líneas Cósmicas',              'SR 2.1.2468 spa',),  # noqa
    (203, 'de', 'Stealth_ger.qmm',          'Tarnvorrichtung',              'SR 2.1.2468 ger',),  # noqa
    (204, 'es', 'Stealth_spa.qmm',          'Sigilo',                       'SR 2.1.2468 spa',),  # noqa
    (205, 'de', 'Svarokok_ger.qmm',         'Swarokok',                     'SR 2.1.2468 ger',),  # noqa
    (206, 'es', 'Svarokok_spa.qmm',         'Swarokok',                     'SR 2.1.2468 spa',),  # noqa
    (207, 'de', 'Xenopark_ger.qmm',         'Xenopark',                     'SR 2.1.2468 ger',),  # noqa
    (208, 'es', 'Xenopark_spa.qmm',         'Xenoparque',                   'SR 2.1.2468 spa',),  # noqa
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
    database.execute_sql('DELETE FROM quest WHERE id >= 139 AND id <= 208')
