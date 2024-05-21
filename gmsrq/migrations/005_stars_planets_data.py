import peewee as pw
from peewee_migrate import Migrator

# @formatter:off
STARS = [
    ( 0, 'en', 'Taron',             'Normal'),  # noqa
    ( 0, 'ru', 'Тарон',             'Normal'),  # noqa
    ( 1, 'en', 'Pkhedoc',           'Normal'),  # noqa
    ( 1, 'ru', 'Пхедок',            'Normal'),  # noqa
    ( 2, 'en', 'Sol',               'Small' ),  # noqa
    ( 2, 'ru', 'Солнце',            'Small' ),  # noqa
    ( 3, 'en', 'Atlas',             'Normal'),  # noqa
    ( 3, 'ru', 'Атлан',             'Normal'),  # noqa
    ( 4, 'en', 'Kraa',              'Small' ),  # noqa
    ( 4, 'ru', 'Краа',              'Small' ),  # noqa
    ( 5, 'en', 'Itsar',             'Small' ),  # noqa
    ( 5, 'ru', 'Ицар',              'Small' ),  # noqa
    ( 6, 'en', 'Mufrid',            'Normal'),  # noqa
    ( 6, 'ru', 'Муфрид',            'Normal'),  # noqa
    ( 7, 'en', 'Fomalhaut',         'Small' ),  # noqa
    ( 7, 'ru', 'Фомальгаут',        'Small' ),  # noqa
    ( 8, 'en', 'Alphard',           'Normal'),  # noqa
    ( 8, 'ru', 'Альфард',           'Normal'),  # noqa
    ( 9, 'en', 'Heze',              'Normal'),  # noqa
    ( 9, 'ru', 'Хезе',              'Normal'),  # noqa
    (10, 'en', 'Rastaban',          'Small' ),  # noqa
    (10, 'ru', 'Растабан',          'Small' ),  # noqa
    (11, 'en', 'Aldiba',            'Normal'),  # noqa
    (11, 'ru', 'Альдиба',           'Normal'),  # noqa
    (12, 'en', 'Schedar',           'Small' ),  # noqa
    (12, 'ru', 'Шедир',             'Small' ),  # noqa
    (13, 'en', 'Canopus',           'Normal'),  # noqa
    (13, 'ru', 'Канопус',           'Normal'),  # noqa
    (14, 'en', 'Avior',             'Small' ),  # noqa
    (14, 'ru', 'Авиор',             'Small' ),  # noqa
    (15, 'en', 'Menkar',            'Normal'),  # noqa
    (15, 'ru', 'Менкар',            'Normal'),  # noqa
    (16, 'en', 'Deneb',             'Small' ),  # noqa
    (16, 'ru', 'Денеб',             'Small' ),  # noqa
    (17, 'en', 'Denebola',          'Normal'),  # noqa
    (17, 'ru', 'Денебола',          'Normal'),  # noqa
    (18, 'en', 'Procyon',           'Small' ),  # noqa
    (18, 'ru', 'Процион',           'Small' ),  # noqa
    (19, 'en', 'Altair',            'Normal'),  # noqa
    (19, 'ru', 'Альтаир',           'Normal'),  # noqa
    (20, 'en', 'Betelgeuse',        'Small' ),  # noqa
    (20, 'ru', 'Бетельгейзе',       'Small' ),  # noqa
    (21, 'en', 'Bellatrix',         'Normal'),  # noqa
    (21, 'ru', 'Беллатрикс',        'Normal'),  # noqa
    (22, 'en', 'Scheat',            'Small' ),  # noqa
    (22, 'ru', 'Шеат',              'Small' ),  # noqa
    (23, 'en', 'Nakkar',            'Normal'),  # noqa
    (23, 'ru', 'Наккар',            'Normal'),  # noqa
    (24, 'en', 'Orion',             'Small' ),  # noqa
    (24, 'ru', 'Орион',             'Small' ),  # noqa
    (25, 'en', 'Alphekka',          'Small' ),  # noqa
    (25, 'ru', 'Алфекка',           'Small' ),  # noqa
    (26, 'en', 'Alioth',            'Normal'),  # noqa
    (26, 'ru', 'Алиот',             'Normal'),  # noqa
    (27, 'en', 'Regulus',           'Normal'),  # noqa
    (27, 'ru', 'Регулус',           'Normal'),  # noqa
    (28, 'en', 'Hamal',             'Normal'),  # noqa
    (28, 'ru', 'Хамаль',            'Normal'),  # noqa
    (29, 'en', 'Akharra',           'Small' ),  # noqa
    (29, 'ru', 'Акхарра',           'Small' ),  # noqa
    (30, 'en', 'Castor',            'Normal'),  # noqa
    (30, 'ru', 'Кастор',            'Normal'),  # noqa
    (31, 'en', 'Marcab',            'Small' ),  # noqa
    (31, 'ru', 'Маркаб',            'Small' ),  # noqa
    (32, 'en', 'Hemni',             'Normal'),  # noqa
    (32, 'ru', 'Хемни',             'Normal'),  # noqa
    (33, 'en', 'Antares',           'Small' ),  # noqa
    (33, 'ru', 'Антарес',           'Small' ),  # noqa
    (34, 'en', 'Atria',             'Normal'),  # noqa
    (34, 'ru', 'Атрия',             'Normal'),  # noqa
    (35, 'en', 'Megrez',            'Small' ),  # noqa
    (35, 'ru', 'Мегрез',            'Small' ),  # noqa
    (36, 'en', 'Pollux',            'Normal'),  # noqa
    (36, 'ru', 'Поллюкс',           'Normal'),  # noqa
    (37, 'en', 'Arts',              'Small' ),  # noqa
    (37, 'ru', 'Арц',               'Small' ),  # noqa
    (38, 'en', 'Cephron',           'Normal'),  # noqa
    (38, 'ru', 'Кефрон',            'Normal'),  # noqa
    (39, 'en', 'Bakhar',            'Small' ),  # noqa
    (39, 'ru', 'Вакхар',            'Small' ),  # noqa
    (40, 'en', 'Vitta Pryonis',     'Normal'),  # noqa
    (40, 'ru', 'Витта Прайонис',    'Normal'),  # noqa
    (41, 'en', 'Hever',             'Small' ),  # noqa
    (41, 'ru', 'Гевер',             'Small' ),  # noqa
    (42, 'en', 'Shomma',            'Normal'),  # noqa
    (42, 'ru', 'Шомма',             'Normal'),  # noqa
    (43, 'en', 'Vinnatrix',         'Small' ),  # noqa
    (43, 'ru', 'Виннатрикс',        'Small' ),  # noqa
    (44, 'en', 'Veles',             'Normal'),  # noqa
    (44, 'ru', 'Велес',             'Normal'),  # noqa
    (45, 'en', 'Tallot',            'Small' ),  # noqa
    (45, 'ru', 'Таллот',            'Small' ),  # noqa
    (46, 'en', 'Arcturus',          'Normal'),  # noqa
    (46, 'ru', 'Арктур',            'Normal'),  # noqa
    (47, 'en', 'Diatar',            'Small' ),  # noqa
    (47, 'ru', 'Диатар',            'Small' ),  # noqa
    (48, 'en', 'Elga',              'Normal'),  # noqa
    (48, 'ru', 'Элга',              'Normal'),  # noqa
    (49, 'en', 'Arcabe',            'Small' ),  # noqa
    (49, 'ru', 'Аркабе',            'Small' ),  # noqa
    (50, 'en', 'Capella',           'Normal'),  # noqa
    (50, 'ru', 'Капелла',           'Normal'),  # noqa
    (51, 'en', 'Arrakis',           'Small' ),  # noqa
    (51, 'ru', 'Арракис',           'Small' ),  # noqa
    (52, 'en', 'Saphrona',          'Normal'),  # noqa
    (52, 'ru', 'Сафрона',           'Normal'),  # noqa
    (53, 'en', 'Al Dagor',          'Small' ),  # noqa
    (53, 'ru', 'Аль Дагор',         'Small' ),  # noqa
    (54, 'en', 'Zavia',             'Small' ),  # noqa
    (54, 'ru', 'Завия',             'Small' ),  # noqa
    (55, 'en', 'Diadem',            'Small' ),  # noqa
    (55, 'ru', 'Диадема',           'Small' ),  # noqa
    (56, 'en', 'Oseum',             'Normal'),  # noqa
    (56, 'ru', 'Озеум',             'Normal'),  # noqa
    (57, 'en', 'Rigel',             'Small' ),  # noqa
    (57, 'ru', 'Ригель',            'Small' ),  # noqa
    (58, 'en', 'Turais',            'Small' ),  # noqa
    (58, 'ru', 'Тураис',            'Small' ),  # noqa
    (59, 'en', 'Celiostre',         'Small' ),  # noqa
    (59, 'ru', 'Селиостр',          'Small' ),  # noqa
    (60, 'en', 'Tzufai',            'Normal'),  # noqa
    (60, 'ru', 'Цуфай',             'Normal'),  # noqa
    (61, 'en', 'Yufalli',           'Normal'),  # noqa
    (61, 'ru', 'Юфалли',            'Normal'),  # noqa
    (62, 'en', 'Murratz',           'Small' ),  # noqa
    (62, 'ru', 'Муррац',            'Small' ),  # noqa
    (63, 'en', 'Minnaver',          'Small' ),  # noqa
    (63, 'ru', 'Миннавер',          'Small' ),  # noqa
    (64, 'en', 'Euron',             'Small' ),  # noqa
    (64, 'ru', 'Эйрон',             'Small' ),  # noqa
    (65, 'en', 'Felgeste',          'Small' ),  # noqa
    (65, 'ru', 'Фелгест',           'Small' ),  # noqa
    (66, 'en', 'Rex',               'Normal'),  # noqa
    (66, 'ru', 'Рекц',              'Normal'),  # noqa
    (67, 'en', 'Sezerke',           'Normal'),  # noqa
    (67, 'ru', 'Сезерк',            'Normal'),  # noqa
    (68, 'en', 'Ukphal',            'Normal'),  # noqa
    (68, 'ru', 'Укфал',             'Normal'),  # noqa
    (69, 'en', 'Sezmen',            'Normal'),  # noqa
    (69, 'ru', 'Сезмен',            'Normal'),  # noqa
    (70, 'en', 'Tortugatz',         'Small' ),  # noqa
    (70, 'ru', 'Тортугац',          'Small' ),  # noqa
    (71, 'en', 'Nifigatz',          'Normal'),  # noqa
    (71, 'ru', 'Нифигац',           'Normal'),  # noqa
]

PLANETS = [
    (  1, 'en', 'Fei',          'Umius'             ),  # noqa
    (  1, 'ru', 'Fei',          'Умий'              ),  # noqa
    (  2, 'en', 'Fei',          'Eipentak'          ),  # noqa
    (  2, 'ru', 'Fei',          'Эйпентак'          ),  # noqa
    (  3, 'en', 'Fei',          'Eilank'            ),  # noqa
    (  3, 'ru', 'Fei',          'Эйланк'            ),  # noqa
    (  4, 'en', 'Fei',          'Aprish'            ),  # noqa
    (  4, 'ru', 'Fei',          'Априш'             ),  # noqa
    (  5, 'en', 'Fei',          'Eneical'           ),  # noqa
    (  5, 'ru', 'Fei',          'Энейкал'           ),  # noqa
    (  6, 'en', 'Fei',          'Ellenta'           ),  # noqa
    (  6, 'ru', 'Fei',          'Эллента'           ),  # noqa
    (  7, 'en', 'Fei',          'Omdey'             ),  # noqa
    (  7, 'ru', 'Fei',          'Омдей'             ),  # noqa
    (  8, 'en', 'Fei',          'Antibius'          ),  # noqa
    (  8, 'ru', 'Fei',          'Антибий'           ),  # noqa
    (  9, 'en', 'Fei',          'Inyand'            ),  # noqa
    (  9, 'ru', 'Fei',          'Иньянд'            ),  # noqa
    ( 10, 'en', 'Fei',          'Akhandish'         ),  # noqa
    ( 10, 'ru', 'Fei',          'Ахандиш'           ),  # noqa
    ( 11, 'en', 'Fei',          'Onnd'              ),  # noqa
    ( 11, 'ru', 'Fei',          'Оннд'              ),  # noqa
    ( 12, 'en', 'Fei',          'Ushalla'           ),  # noqa
    ( 12, 'ru', 'Fei',          'Ушалла'            ),  # noqa
    ( 13, 'en', 'Fei',          'Inderon'           ),  # noqa
    ( 13, 'ru', 'Fei',          'Индерон'           ),  # noqa
    ( 14, 'en', 'Fei',          'Eimanapolon'       ),  # noqa
    ( 14, 'ru', 'Fei',          'Эйманаполон'       ),  # noqa
    ( 15, 'en', 'Fei',          'Alganak'           ),  # noqa
    ( 15, 'ru', 'Fei',          'Алганак'           ),  # noqa
    ( 16, 'en', 'Fei',          'Ummaden'           ),  # noqa
    ( 16, 'ru', 'Fei',          'Уммадан'           ),  # noqa
    ( 17, 'en', 'Fei',          'Eif'               ),  # noqa
    ( 17, 'ru', 'Fei',          'Эйф'               ),  # noqa
    ( 18, 'en', 'Fei',          'Eshnink'           ),  # noqa
    ( 18, 'ru', 'Fei',          'Эшнинк'            ),  # noqa
    ( 19, 'en', 'Fei',          'Alyanony'          ),  # noqa
    ( 19, 'ru', 'Fei',          'Альянони'          ),  # noqa
    ( 20, 'en', 'Fei',          'Egmer'             ),  # noqa
    ( 20, 'ru', 'Fei',          'Эгмер'             ),  # noqa
    ( 21, 'en', 'Fei',          'Itniglue'          ),  # noqa
    ( 21, 'ru', 'Fei',          'Итниклей'          ),  # noqa
    ( 22, 'en', 'Fei',          'Lantinda'          ),  # noqa
    ( 22, 'ru', 'Fei',          'Лантинда'          ),  # noqa
    ( 23, 'en', 'Fei',          'Umartanish'        ),  # noqa
    ( 23, 'ru', 'Fei',          'Умартаниш'         ),  # noqa
    ( 24, 'en', 'Fei',          'Asasot'            ),  # noqa
    ( 24, 'ru', 'Fei',          'Асасот'            ),  # noqa
    ( 25, 'en', 'Fei',          'Unnun'             ),  # noqa
    ( 25, 'ru', 'Fei',          'Уннун'             ),  # noqa
    ( 26, 'en', 'Fei',          'Igmeirish'         ),  # noqa
    ( 26, 'ru', 'Fei',          'Игмейриш'          ),  # noqa
    ( 27, 'en', 'Fei',          'Inklada'           ),  # noqa
    ( 27, 'ru', 'Fei',          'Инклада'           ),  # noqa
    ( 28, 'en', 'Fei',          'Ammark'            ),  # noqa
    ( 28, 'ru', 'Fei',          'Аммарк'            ),  # noqa
    ( 29, 'en', 'Fei',          'Uzuny'             ),  # noqa
    ( 29, 'ru', 'Fei',          'Узуни'             ),  # noqa
    ( 30, 'en', 'Fei',          'Irinia'            ),  # noqa
    ( 30, 'ru', 'Fei',          'Ириниа'            ),  # noqa
    ( 31, 'en', 'Fei',          'Efeimel'           ),  # noqa
    ( 31, 'ru', 'Fei',          'Эфэймел'           ),  # noqa
    ( 32, 'en', 'Fei',          'Eidango'           ),  # noqa
    ( 32, 'ru', 'Fei',          'Айданго'           ),  # noqa
    # 33
    # 34
    ( 35, 'en', 'Fei',          'Ikhinsh'           ),  # noqa
    ( 35, 'ru', 'Fei',          'Ихинш'             ),  # noqa
    ( 36, 'en', 'Fei',          'Ornalish'          ),  # noqa
    ( 36, 'ru', 'Fei',          'Орналиш'           ),  # noqa
    ( 37, 'en', 'Fei',          'Emzema'            ),  # noqa
    ( 37, 'ru', 'Fei',          'Эмзема'            ),  # noqa
    ( 38, 'en', 'Fei',          'Asyan'             ),  # noqa
    ( 38, 'ru', 'Fei',          'Асьян'             ),  # noqa
    ( 39, 'en', 'Fei',          'Ilgadok'           ),  # noqa
    ( 39, 'ru', 'Fei',          'Илгадак'           ),  # noqa
    ( 40, 'en', 'Fei',          'Ulliallyan'        ),  # noqa
    ( 40, 'ru', 'Fei',          'Улиаллян'          ),  # noqa
    ( 41, 'en', 'Fei',          'Eizagondin'        ),  # noqa
    ( 41, 'ru', 'Fei',          'Айзагондин'        ),  # noqa
    ( 42, 'en', 'Fei',          'Ishgibnul'         ),  # noqa
    ( 42, 'ru', 'Fei',          'Ишгибнул'          ),  # noqa
    ( 43, 'en', 'Fei',          'Efmma'             ),  # noqa
    ( 43, 'ru', 'Fei',          'Эфмма'             ),  # noqa
    ( 44, 'en', 'Fei',          'Ukkunay'           ),  # noqa
    ( 44, 'ru', 'Fei',          'Уккунай'           ),  # noqa
    ( 45, 'en', 'Fei',          'Ezeban'            ),  # noqa
    ( 45, 'ru', 'Fei',          'Эзэбан'            ),  # noqa
    ( 46, 'en', 'Fei',          'Ominena'           ),  # noqa
    ( 46, 'ru', 'Fei',          'Оминена'           ),  # noqa
    ( 47, 'en', 'Fei',          'Agleya'            ),  # noqa
    ( 47, 'ru', 'Fei',          'Аглея'             ),  # noqa
    ( 48, 'en', 'Fei',          'Onderansh'         ),  # noqa
    ( 48, 'ru', 'Fei',          'Ондеранш'          ),  # noqa
    ( 49, 'en', 'Fei',          'Ulgeuny'           ),  # noqa
    ( 49, 'ru', 'Fei',          'Улгеуни'           ),  # noqa
    ( 50, 'en', 'Fei',          'Ilgos'             ),  # noqa
    ( 50, 'ru', 'Fei',          'Илгос'             ),  # noqa
    ( 51, 'en', 'Fei',          'Agunnish'          ),  # noqa
    ( 51, 'ru', 'Fei',          'Агунниш'           ),  # noqa
    ( 52, 'en', 'Fei',          'Ezilenk'           ),  # noqa
    ( 52, 'ru', 'Fei',          'Эзиленк'           ),  # noqa
    ( 53, 'en', 'Fei',          'Undanka'           ),  # noqa
    ( 53, 'ru', 'Fei',          'Унданка'           ),  # noqa
    ( 54, 'en', 'Fei',          'Izhaita'           ),  # noqa
    ( 54, 'ru', 'Fei',          'Ижаита'            ),  # noqa
    ( 55, 'en', 'Fei',          'Oprenin'           ),  # noqa
    ( 55, 'ru', 'Fei',          'Опренин'           ),  # noqa
    ( 56, 'en', 'Fei',          'Affam'             ),  # noqa
    ( 56, 'ru', 'Fei',          'Аффам'             ),  # noqa
    ( 57, 'en', 'Fei',          'Ontakalany'        ),  # noqa
    ( 57, 'ru', 'Fei',          'Онтакалани'        ),  # noqa
    ( 58, 'en', 'Fei',          'Uditamire'         ),  # noqa
    ( 58, 'ru', 'Fei',          'Удитамир'          ),  # noqa
    ( 59, 'en', 'Fei',          'Upraney'           ),  # noqa
    ( 59, 'ru', 'Fei',          'Упранай'           ),  # noqa
    ( 60, 'en', 'Fei',          'Eshikul'           ),  # noqa
    ( 60, 'ru', 'Fei',          'Эшшикул'           ),  # noqa
    ( 61, 'en', 'Fei',          'Angoley'           ),  # noqa
    ( 61, 'ru', 'Fei',          'Анголай'           ),  # noqa
    ( 62, 'en', 'Fei',          'Omyala'            ),  # noqa
    ( 62, 'ru', 'Fei',          'Омьяла'            ),  # noqa
    ( 63, 'en', 'Fei',          'Ezhidan'           ),  # noqa
    ( 63, 'ru', 'Fei',          'Эжидан'            ),  # noqa
    ( 64, 'en', 'Fei',          'Uglakha'           ),  # noqa
    ( 64, 'ru', 'Fei',          'Углаха'            ),  # noqa
    ( 65, 'en', 'Fei',          'Izitry'            ),  # noqa
    ( 65, 'ru', 'Fei',          'Изитри'            ),  # noqa
    ( 66, 'en', 'Fei',          'Elkada'            ),  # noqa
    ( 66, 'ru', 'Fei',          'Элкада'            ),  # noqa
    ( 67, 'en', 'Fei',          'Alice'             ),  # noqa
    ( 67, 'ru', 'Fei',          'Алис'              ),  # noqa
    ( 68, 'en', 'Fei',          'Unganamerun'       ),  # noqa
    ( 68, 'ru', 'Fei',          'Унганамерун'       ),  # noqa
    ( 69, 'en', 'Fei',          'Erpagey'           ),  # noqa
    ( 69, 'ru', 'Fei',          'Эрпагай'           ),  # noqa
    ( 70, 'en', 'Fei',          'Apr'               ),  # noqa
    ( 70, 'ru', 'Fei',          'Апр'               ),  # noqa
    (  1, 'en', 'Gaal',         'Duede'             ),  # noqa
    (  1, 'ru', 'Gaal',         'Дуэдэ'             ),  # noqa
    (  2, 'en', 'Gaal',         'Hahaldock'         ),  # noqa
    (  2, 'ru', 'Gaal',         'Гаалдок'           ),  # noqa
    (  3, 'en', 'Gaal',         'Banana'            ),  # noqa
    (  3, 'ru', 'Gaal',         'Банана'            ),  # noqa
    (  4, 'en', 'Gaal',         'Bohoz'             ),  # noqa
    (  4, 'ru', 'Gaal',         'Бооз'              ),  # noqa
    (  5, 'en', 'Gaal',         'Zoholto'           ),  # noqa
    (  5, 'ru', 'Gaal',         'Зоолто'            ),  # noqa
    (  6, 'en', 'Gaal',         'Rahalito'          ),  # noqa
    (  6, 'ru', 'Gaal',         'Раалито'           ),  # noqa
    (  7, 'en', 'Gaal',         'Mederito'          ),  # noqa
    (  7, 'ru', 'Gaal',         'Мэдэрито'          ),  # noqa
    (  8, 'en', 'Gaal',         'Rohoka'            ),  # noqa
    (  8, 'ru', 'Gaal',         'Роока'             ),  # noqa
    (  9, 'en', 'Gaal',         'Menecato'          ),  # noqa
    (  9, 'ru', 'Gaal',         'Мэнэкато'          ),  # noqa
    ( 10, 'en', 'Gaal',         'Heina'             ),  # noqa
    ( 10, 'ru', 'Gaal',         'Гайна'             ),  # noqa
    ( 11, 'en', 'Gaal',         'Zaha'              ),  # noqa
    ( 11, 'ru', 'Gaal',         'Заа'               ),  # noqa
    ( 12, 'en', 'Gaal',         'Zemin'             ),  # noqa
    ( 12, 'ru', 'Gaal',         'Зэмин'             ),  # noqa
    ( 13, 'en', 'Gaal',         'Redea'             ),  # noqa
    ( 13, 'ru', 'Gaal',         'Рэдэа'             ),  # noqa
    ( 14, 'en', 'Gaal',         'Pune-anita'        ),  # noqa
    ( 14, 'ru', 'Gaal',         'Пунэ-анита'        ),  # noqa
    ( 15, 'en', 'Gaal',         'Sialla'            ),  # noqa
    ( 15, 'ru', 'Gaal',         'Сиалла'            ),  # noqa
    ( 16, 'en', 'Gaal',         'Tolt-Hain'         ),  # noqa
    ( 16, 'ru', 'Gaal',         'Толт-гаин'         ),  # noqa
    ( 17, 'en', 'Gaal',         'Riolky'            ),  # noqa
    ( 17, 'ru', 'Gaal',         'Риолки'            ),  # noqa
    ( 18, 'en', 'Gaal',         'Uhudlana'          ),  # noqa
    ( 18, 'ru', 'Gaal',         'Уудлана'           ),  # noqa
    ( 19, 'en', 'Gaal',         'Palteomeo'         ),  # noqa
    ( 19, 'ru', 'Gaal',         'Палтеомео'         ),  # noqa
    ( 20, 'en', 'Gaal',         'Zapahas'           ),  # noqa
    ( 20, 'ru', 'Gaal',         'Запаас'            ),  # noqa
    ( 21, 'en', 'Gaal',         'Orohogen'          ),  # noqa
    ( 21, 'ru', 'Gaal',         'Орооген'           ),  # noqa
    ( 22, 'en', 'Gaal',         'Ilohoka'           ),  # noqa
    ( 22, 'ru', 'Gaal',         'Илоока'            ),  # noqa
    ( 23, 'en', 'Gaal',         'Prohont'           ),  # noqa
    ( 23, 'ru', 'Gaal',         'Проон'             ),  # noqa
    ( 24, 'en', 'Gaal',         'Eluana'            ),  # noqa
    ( 24, 'ru', 'Gaal',         'Элуана'            ),  # noqa
    ( 25, 'en', 'Gaal',         'Letamay'           ),  # noqa
    ( 25, 'ru', 'Gaal',         'Летамаи'           ),  # noqa
    ( 26, 'en', 'Gaal',         'Lienay-va'         ),  # noqa
    ( 26, 'ru', 'Gaal',         'Лиеная-ва'         ),  # noqa
    ( 27, 'en', 'Gaal',         'Keyinaha'          ),  # noqa
    ( 27, 'ru', 'Gaal',         'Кэйинаа'           ),  # noqa
    ( 28, 'en', 'Gaal',         'Euruahat'          ),  # noqa
    ( 28, 'ru', 'Gaal',         'Эуруаат'           ),  # noqa
    ( 29, 'en', 'Gaal',         'Kaliontoho'        ),  # noqa
    ( 29, 'ru', 'Gaal',         'Калионтоо'         ),  # noqa
    ( 30, 'en', 'Gaal',         'Rohol'             ),  # noqa
    ( 30, 'ru', 'Gaal',         'Роол'              ),  # noqa
    ( 31, 'en', 'Gaal',         'Rantahas'          ),  # noqa
    ( 31, 'ru', 'Gaal',         'Рантаас'           ),  # noqa
    ( 32, 'en', 'Gaal',         'Galteya'           ),  # noqa
    ( 32, 'ru', 'Gaal',         'Галтайя'           ),  # noqa
    ( 33, 'en', 'Gaal',         'Oto-rara'          ),  # noqa
    ( 33, 'ru', 'Gaal',         'Ото-рара'          ),  # noqa
    ( 34, 'en', 'Gaal',         'Unotaka'           ),  # noqa
    ( 34, 'ru', 'Gaal',         'Унотака'           ),  # noqa
    ( 35, 'en', 'Gaal',         'Ha-poe'            ),  # noqa
    ( 35, 'ru', 'Gaal',         'Га-по'             ),  # noqa
    ( 36, 'en', 'Gaal',         'Sholohany'         ),  # noqa
    ( 36, 'ru', 'Gaal',         'Шолоани'           ),  # noqa
    ( 37, 'en', 'Gaal',         'Hail-otny'         ),  # noqa
    ( 37, 'ru', 'Gaal',         'Гаил-отни'         ),  # noqa
    ( 38, 'en', 'Gaal',         'Ihiltaya'          ),  # noqa
    ( 38, 'ru', 'Gaal',         'Иилтайя'           ),  # noqa
    ( 39, 'en', 'Gaal',         'Siloho'            ),  # noqa
    ( 39, 'ru', 'Gaal',         'Силоо'             ),  # noqa
    ( 40, 'en', 'Gaal',         'Lu-pupurue'        ),  # noqa
    ( 40, 'ru', 'Gaal',         'Лу-пуру'           ),  # noqa
    ( 41, 'en', 'Gaal',         'Zavay'             ),  # noqa
    ( 41, 'ru', 'Gaal',         'Заваи'             ),  # noqa
    ( 42, 'en', 'Gaal',         'Elle'              ),  # noqa
    ( 42, 'ru', 'Gaal',         'Эллэ'              ),  # noqa
    ( 43, 'en', 'Gaal',         'Lyusyahan'         ),  # noqa
    ( 43, 'ru', 'Gaal',         'Люсьяан'           ),  # noqa
    ( 44, 'en', 'Gaal',         'Onghe-ammia'       ),  # noqa
    ( 44, 'ru', 'Gaal',         'Онге-аммиа'        ),  # noqa
    ( 45, 'en', 'Gaal',         'Avihine'           ),  # noqa
    ( 45, 'ru', 'Gaal',         'Авиинэ'            ),  # noqa
    ( 46, 'en', 'Gaal',         'Abeva'             ),  # noqa
    ( 46, 'ru', 'Gaal',         'Абэва'             ),  # noqa
    ( 47, 'en', 'Gaal',         'Ulry-anit'         ),  # noqa
    ( 47, 'ru', 'Gaal',         'Улри-анит'         ),  # noqa
    ( 48, 'en', 'Gaal',         'Arty-lit'          ),  # noqa
    ( 48, 'ru', 'Gaal',         'Арти-лит'          ),  # noqa
    ( 49, 'en', 'Gaal',         'Bre-gedne'         ),  # noqa
    ( 49, 'ru', 'Gaal',         'Брэ-гедне'         ),  # noqa
    ( 50, 'en', 'Gaal',         'Sualy'             ),  # noqa
    ( 50, 'ru', 'Gaal',         'Суали'             ),  # noqa
    ( 51, 'en', 'Gaal',         'Aha-ogy'           ),  # noqa
    ( 51, 'ru', 'Gaal',         'Аа-оги'            ),  # noqa
    ( 52, 'en', 'Gaal',         'Dana-ia'           ),  # noqa
    ( 52, 'ru', 'Gaal',         'Дана-иа'           ),  # noqa
    ( 53, 'en', 'Gaal',         'Hasyain'           ),  # noqa
    ( 53, 'ru', 'Gaal',         'Гасьяин'           ),  # noqa
    ( 54, 'en', 'Gaal',         'Litt-umia'         ),  # noqa
    ( 54, 'ru', 'Gaal',         'Литт-умиа'         ),  # noqa
    ( 55, 'en', 'Gaal',         'Danio'             ),  # noqa
    ( 55, 'ru', 'Gaal',         'Данио'             ),  # noqa
    ( 56, 'en', 'Gaal',         'Enoro-init'        ),  # noqa
    ( 56, 'ru', 'Gaal',         'Эноро-инит'        ),  # noqa
    ( 57, 'en', 'Gaal',         'Linia'             ),  # noqa
    ( 57, 'ru', 'Gaal',         'Линиа'             ),  # noqa
    ( 58, 'en', 'Gaal',         'Ranto-mune'        ),  # noqa
    ( 58, 'ru', 'Gaal',         'Ранто-муна'        ),  # noqa
    ( 59, 'en', 'Gaal',         'Hohol-ana'         ),  # noqa
    ( 59, 'ru', 'Gaal',         'Гоол-ана'          ),  # noqa
    ( 60, 'en', 'Gaal',         'Almahan-uteb'      ),  # noqa
    ( 60, 'ru', 'Gaal',         'Алмаан-утэ'        ),  # noqa
    ( 61, 'en', 'Gaal',         'Aurumea'           ),  # noqa
    ( 61, 'ru', 'Gaal',         'Аурумэа'           ),  # noqa
    ( 62, 'en', 'Gaal',         'Ias-anata'         ),  # noqa
    ( 62, 'ru', 'Gaal',         'Иас-аната'         ),  # noqa
    ( 63, 'en', 'Gaal',         'Glassee-nai'       ),  # noqa
    ( 63, 'ru', 'Gaal',         'Глассии-наи'       ),  # noqa
    ( 64, 'en', 'Gaal',         'Alloro-bisty'      ),  # noqa
    ( 64, 'ru', 'Gaal',         'Аллоро-бисти'      ),  # noqa
    ( 65, 'en', 'Gaal',         'Pudrue-oi'         ),  # noqa
    ( 65, 'ru', 'Gaal',         'Пудру-ои'          ),  # noqa
    ( 66, 'en', 'Gaal',         'Omaky-ena'         ),  # noqa
    ( 66, 'ru', 'Gaal',         'Омаки-ена'         ),  # noqa
    ( 67, 'en', 'Gaal',         'Favvap-og'         ),  # noqa
    ( 67, 'ru', 'Gaal',         'Фаввап-ог'         ),  # noqa
    ( 68, 'en', 'Gaal',         'Sitra-ahando'      ),  # noqa
    ( 68, 'ru', 'Gaal',         'Ситра-аандо'       ),  # noqa
    ( 69, 'en', 'Gaal',         'Gashtik-china'     ),  # noqa
    ( 69, 'ru', 'Gaal',         'Гаштик-чина'       ),  # noqa
    ( 70, 'en', 'Gaal',         'Lipa-iuy'          ),  # noqa
    ( 70, 'ru', 'Gaal',         'Липа-иуи'          ),  # noqa
    (  1, 'en', 'Maloc',        'Arnarick Guadad'   ),  # noqa
    (  1, 'ru', 'Maloc',        'Арнарик Гаудад'    ),  # noqa
    (  2, 'en', 'Maloc',        'Ramgatrue'         ),  # noqa
    (  2, 'ru', 'Maloc',        'Рамгатру'          ),  # noqa
    (  3, 'en', 'Maloc',        'Protue Pamperoy'   ),  # noqa
    (  3, 'ru', 'Maloc',        'Проту Памперой'    ),  # noqa
    (  4, 'en', 'Maloc',        'Dreadnue-astan'    ),  # noqa
    (  4, 'ru', 'Maloc',        'Дрэдну-астан'      ),  # noqa
    (  5, 'en', 'Maloc',        'Zantak'            ),  # noqa
    (  5, 'ru', 'Maloc',        'Зэнтак'            ),  # noqa
    (  6, 'en', 'Maloc',        'Orstue-odid'       ),  # noqa
    (  6, 'ru', 'Maloc',        'Орсту-оудид'       ),  # noqa
    (  7, 'en', 'Maloc',        'Tanntack Pampart'  ),  # noqa
    (  7, 'ru', 'Maloc',        'Тантак Тампарт'    ),  # noqa
    (  8, 'en', 'Maloc',        'Godiue Pratue'     ),  # noqa
    (  8, 'ru', 'Maloc',        'Гордиу Прэту'      ),  # noqa
    (  9, 'en', 'Maloc',        'Oider-amarod'      ),  # noqa
    (  9, 'ru', 'Maloc',        'Ойдэр-амарод'      ),  # noqa
    ( 10, 'en', 'Maloc',        'Graneka'           ),  # noqa
    ( 10, 'ru', 'Maloc',        'Гранэка'           ),  # noqa
    ( 11, 'en', 'Maloc',        'Trigit-augro'      ),  # noqa
    ( 11, 'ru', 'Maloc',        'Тригит-аугро'      ),  # noqa
    ( 12, 'en', 'Maloc',        'Khanoy'            ),  # noqa
    ( 12, 'ru', 'Maloc',        'Ханой'             ),  # noqa
    ( 13, 'en', 'Maloc',        'Trad Rack'         ),  # noqa
    ( 13, 'ru', 'Maloc',        'Трад Рраг'         ),  # noqa
    ( 14, 'en', 'Maloc',        'Aikharrue Meddona' ),  # noqa
    ( 14, 'ru', 'Maloc',        'Айхарру Меддона'   ),  # noqa
    ( 15, 'en', 'Maloc',        'Arracka Gatrue'    ),  # noqa
    ( 15, 'ru', 'Maloc',        'Аррака Гатру'      ),  # noqa
    ( 16, 'en', 'Maloc',        'Knetue'            ),  # noqa
    ( 16, 'ru', 'Maloc',        'Кнэту'             ),  # noqa
    ( 17, 'en', 'Maloc',        'Grnadock-umack'    ),  # noqa
    ( 17, 'ru', 'Maloc',        'Грнадок-умак'      ),  # noqa
    ( 18, 'en', 'Maloc',        'Ursana Guss'       ),  # noqa
    ( 18, 'ru', 'Maloc',        'Урсана Гусс'       ),  # noqa
    ( 19, 'en', 'Maloc',        'Mabel'             ),  # noqa
    ( 19, 'ru', 'Maloc',        'Мабэл'             ),  # noqa
    ( 20, 'en', 'Maloc',        'Oiknur Bad'        ),  # noqa
    ( 20, 'ru', 'Maloc',        'Ойкнур Бад'        ),  # noqa
    ( 21, 'en', 'Maloc',        'Shega Krie'        ),  # noqa
    ( 21, 'ru', 'Maloc',        'Шэга Кри'          ),  # noqa
    ( 22, 'en', 'Maloc',        'Malary'            ),  # noqa
    ( 22, 'ru', 'Maloc',        'Малари'            ),  # noqa
    ( 23, 'en', 'Maloc',        'Urda Gal'          ),  # noqa
    ( 23, 'ru', 'Maloc',        'Урда Гал'          ),  # noqa
    ( 24, 'en', 'Maloc',        'Zarik Mugund'      ),  # noqa
    ( 24, 'ru', 'Maloc',        'Зарик Мугудун'     ),  # noqa
    ( 25, 'en', 'Maloc',        'Dna Gurand'        ),  # noqa
    ( 25, 'ru', 'Maloc',        'Дна Гуранд'        ),  # noqa
    ( 26, 'en', 'Maloc',        'Umanit'            ),  # noqa
    ( 26, 'ru', 'Maloc',        'Уманит'            ),  # noqa
    ( 27, 'en', 'Maloc',        'Ugrar Lato'        ),  # noqa
    ( 27, 'ru', 'Maloc',        'Уграр Лато'        ),  # noqa
    ( 28, 'en', 'Maloc',        'Zunuassod'         ),  # noqa
    ( 28, 'ru', 'Maloc',        'Зунуассод'         ),  # noqa
    ( 29, 'en', 'Maloc',        'Arragid-asda'      ),  # noqa
    ( 29, 'ru', 'Maloc',        'Аррагид-асда'      ),  # noqa
    ( 30, 'en', 'Maloc',        'Samtarue'          ),  # noqa
    ( 30, 'ru', 'Maloc',        'Самтару'           ),  # noqa
    ( 31, 'en', 'Maloc',        'Dagod'             ),  # noqa
    ( 31, 'ru', 'Maloc',        'Дагод'             ),  # noqa
    ( 32, 'en', 'Maloc',        'Predid Rukanay'    ),  # noqa
    ( 32, 'ru', 'Maloc',        'Прэдид Руканай'    ),  # noqa
    ( 33, 'en', 'Maloc',        'Dakot Rukanay'     ),  # noqa
    ( 33, 'ru', 'Maloc',        'Дакот Руканай'     ),  # noqa
    ( 34, 'en', 'Maloc',        'Sabzda Rukanay'    ),  # noqa
    ( 34, 'ru', 'Maloc',        'Сабзда Руканай'    ),  # noqa
    ( 35, 'en', 'Maloc',        'Ikhmeg-ello'       ),  # noqa
    ( 35, 'ru', 'Maloc',        'Ихмег-элло'        ),  # noqa
    ( 36, 'en', 'Maloc',        'Iruzgartod'        ),  # noqa
    ( 36, 'ru', 'Maloc',        'Ирузгартод'        ),  # noqa
    ( 37, 'en', 'Maloc',        'Gont Marin'        ),  # noqa
    ( 37, 'ru', 'Maloc',        'Гонт Марин'        ),  # noqa
    ( 38, 'en', 'Maloc',        'Vaxie-arnalue'     ),  # noqa
    ( 38, 'ru', 'Maloc',        'Вакси-арналу'      ),  # noqa
    ( 39, 'en', 'Maloc',        'Zadlort'           ),  # noqa
    ( 39, 'ru', 'Maloc',        'Задлорт'           ),  # noqa
    ( 40, 'en', 'Maloc',        'Akhmanoy Prekty'   ),  # noqa
    ( 40, 'ru', 'Maloc',        'Ахманой Прэкти'    ),  # noqa
    ( 41, 'en', 'Maloc',        'Mogpin Roe'        ),  # noqa
    ( 41, 'ru', 'Maloc',        'Могпин Роу'        ),  # noqa
    ( 42, 'en', 'Maloc',        'Gdul-onrold'       ),  # noqa
    ( 42, 'ru', 'Maloc',        'Гдул-онролд'       ),  # noqa
    ( 43, 'en', 'Maloc',        'Ellatna Marko'     ),  # noqa
    ( 43, 'ru', 'Maloc',        'Эллатна Марко'     ),  # noqa
    ( 44, 'en', 'Maloc',        'Zagedit'           ),  # noqa
    ( 44, 'ru', 'Maloc',        'Загэдит'           ),  # noqa
    ( 45, 'en', 'Maloc',        'Kmertil'           ),  # noqa
    ( 45, 'ru', 'Maloc',        'Кмэртил'           ),  # noqa
    ( 46, 'en', 'Maloc',        'Pra-abiynitz'      ),  # noqa
    ( 46, 'ru', 'Maloc',        'Пра-абийнит'       ),  # noqa
    ( 47, 'en', 'Maloc',        'Khazenna'          ),  # noqa
    ( 47, 'ru', 'Maloc',        'Хазэнна'           ),  # noqa
    ( 48, 'en', 'Maloc',        'Virt'              ),  # noqa
    ( 48, 'ru', 'Maloc',        'Вирт'              ),  # noqa
    ( 49, 'en', 'Maloc',        'In-akrenly'        ),  # noqa
    ( 49, 'ru', 'Maloc',        'Ин-акрэнли'        ),  # noqa
    ( 50, 'en', 'Maloc',        'Latot Kiramas'     ),  # noqa
    ( 50, 'ru', 'Maloc',        'Латот Кирамас'     ),  # noqa
    ( 51, 'en', 'Maloc',        'Gragodr'           ),  # noqa
    ( 51, 'ru', 'Maloc',        'Грагодр'           ),  # noqa
    ( 52, 'en', 'Maloc',        'Brobis Danue'      ),  # noqa
    ( 52, 'ru', 'Maloc',        'Бробис Дану'       ),  # noqa
    ( 53, 'en', 'Maloc',        'Yuzhdana-melis'    ),  # noqa
    ( 53, 'ru', 'Maloc',        'Юждана-мэлис'      ),  # noqa
    ( 54, 'en', 'Maloc',        'Raptenty'          ),  # noqa
    ( 54, 'ru', 'Maloc',        'Раптенти'          ),  # noqa
    ( 55, 'en', 'Maloc',        'Barracard'         ),  # noqa
    ( 55, 'ru', 'Maloc',        'Барракарта'        ),  # noqa
    ( 56, 'en', 'Maloc',        'Tristie'           ),  # noqa
    ( 56, 'ru', 'Maloc',        'Тристи'            ),  # noqa
    ( 57, 'en', 'Maloc',        'Vagdity'           ),  # noqa
    ( 57, 'ru', 'Maloc',        'Вагдитай'          ),  # noqa
    ( 58, 'en', 'Maloc',        'Enue-aprigga'      ),  # noqa
    ( 58, 'ru', 'Maloc',        'Эну-апригга'       ),  # noqa
    ( 59, 'en', 'Maloc',        'Khrakundo-mayra'   ),  # noqa
    ( 59, 'ru', 'Maloc',        'Хракундо-майра'    ),  # noqa
    ( 60, 'en', 'Maloc',        'Berinar Dag'       ),  # noqa
    ( 60, 'ru', 'Maloc',        'Беринар Даг'       ),  # noqa
    ( 61, 'en', 'Maloc',        'Vactos'            ),  # noqa
    ( 61, 'ru', 'Maloc',        'Вактос'            ),  # noqa
    ( 62, 'en', 'Maloc',        'Drashta Rongy'     ),  # noqa
    ( 62, 'ru', 'Maloc',        'Драшта Ронги'      ),  # noqa
    ( 63, 'en', 'Maloc',        'Hemert'            ),  # noqa
    ( 63, 'ru', 'Maloc',        'Гемерт'            ),  # noqa
    ( 64, 'en', 'Maloc',        'Mirroky'           ),  # noqa
    ( 64, 'ru', 'Maloc',        'Мирроки'           ),  # noqa
    ( 65, 'en', 'Maloc',        'Kudladra Gad'      ),  # noqa
    ( 65, 'ru', 'Maloc',        'Кудладра Гад'      ),  # noqa
    ( 66, 'en', 'Maloc',        'Suzhtue-ogy'       ),  # noqa
    ( 66, 'ru', 'Maloc',        'Зушту-оуги'        ),  # noqa
    ( 67, 'en', 'Maloc',        'Tissie Rad'        ),  # noqa
    ( 67, 'ru', 'Maloc',        'Тисси Рад'         ),  # noqa
    ( 68, 'en', 'Maloc',        'Lestang'           ),  # noqa
    ( 68, 'ru', 'Maloc',        'Лестанг'           ),  # noqa
    ( 69, 'en', 'Maloc',        'Prakinroy'         ),  # noqa
    ( 69, 'ru', 'Maloc',        'Пракинрой'         ),  # noqa
    ( 70, 'en', 'Maloc',        'Dnoriue Gadzeka'   ),  # noqa
    ( 70, 'ru', 'Maloc',        'Днориу Гадзека'    ),  # noqa
    (  1, 'en', 'No',           'Hartis'            ),  # noqa
    (  1, 'ru', 'No',           'Хартис'            ),  # noqa
    (  2, 'en', 'No',           'Kalayna'           ),  # noqa
    (  2, 'ru', 'No',           'Калайна'           ),  # noqa
    (  3, 'en', 'No',           'Unashera'          ),  # noqa
    (  3, 'ru', 'No',           'Унашера'           ),  # noqa
    (  4, 'en', 'No',           'Vang'              ),  # noqa
    (  4, 'ru', 'No',           'Ванг'              ),  # noqa
    (  5, 'en', 'No',           'Preston'           ),  # noqa
    (  5, 'ru', 'No',           'Престон'           ),  # noqa
    (  6, 'en', 'No',           'Daitola'           ),  # noqa
    (  6, 'ru', 'No',           'Дайтола'           ),  # noqa
    (  7, 'en', 'No',           'Uvadol'            ),  # noqa
    (  7, 'ru', 'No',           'Увадол'            ),  # noqa
    (  8, 'en', 'No',           'Listin'            ),  # noqa
    (  8, 'ru', 'No',           'Листин'            ),  # noqa
    (  9, 'en', 'No',           'Uzza'              ),  # noqa
    (  9, 'ru', 'No',           'Узза'              ),  # noqa
    ( 10, 'en', 'No',           'Amicle'            ),  # noqa
    ( 10, 'ru', 'No',           'Амикл'             ),  # noqa
    ( 11, 'en', 'No',           'Ciney'             ),  # noqa
    ( 11, 'ru', 'No',           'Цинея'             ),  # noqa
    ( 12, 'en', 'No',           'Eizas'             ),  # noqa
    ( 12, 'ru', 'No',           'Айзас'             ),  # noqa
    ( 13, 'en', 'No',           'Parakeldo'         ),  # noqa
    ( 13, 'ru', 'No',           'Паракелдо'         ),  # noqa
    ( 14, 'en', 'No',           'Zharnue'           ),  # noqa
    ( 14, 'ru', 'No',           'Жарну'             ),  # noqa
    ( 15, 'en', 'No',           'Raneprone'         ),  # noqa
    ( 15, 'ru', 'No',           'Ранепрон'          ),  # noqa
    ( 16, 'en', 'No',           'Mersis'            ),  # noqa
    ( 16, 'ru', 'No',           'Мерисис'           ),  # noqa
    ( 17, 'en', 'No',           'Mulnao'            ),  # noqa
    ( 17, 'ru', 'No',           'Мулнао'            ),  # noqa
    ( 18, 'en', 'No',           'Pkhaty'            ),  # noqa
    ( 18, 'ru', 'No',           'Пхати'             ),  # noqa
    ( 19, 'en', 'No',           'Bernut'            ),  # noqa
    ( 19, 'ru', 'No',           'Бернут'            ),  # noqa
    ( 20, 'en', 'No',           'Aina-vera'         ),  # noqa
    ( 20, 'ru', 'No',           'Айна-вера'         ),  # noqa
    ( 21, 'en', 'No',           'Gungana'           ),  # noqa
    ( 21, 'ru', 'No',           'Гунгана'           ),  # noqa
    ( 22, 'en', 'No',           'Zanland'           ),  # noqa
    ( 22, 'ru', 'No',           'Занландия'         ),  # noqa
    ( 23, 'en', 'No',           'Roksha'            ),  # noqa
    ( 23, 'ru', 'No',           'Рокша'             ),  # noqa
    ( 24, 'en', 'No',           'Littie'            ),  # noqa
    ( 24, 'ru', 'No',           'Литти'             ),  # noqa
    ( 25, 'en', 'No',           'Gangador'          ),  # noqa
    ( 25, 'ru', 'No',           'Хангадор'          ),  # noqa
    ( 26, 'en', 'No',           'Yukka'             ),  # noqa
    ( 26, 'ru', 'No',           'Юкка'              ),  # noqa
    ( 27, 'en', 'No',           'Comegetsome'       ),  # noqa
    ( 27, 'ru', 'No',           'Выньдабрось'       ),  # noqa
    ( 28, 'en', 'No',           'Fankor'            ),  # noqa
    ( 28, 'ru', 'No',           'Фанкор'            ),  # noqa
    ( 29, 'en', 'No',           'Yalgaza'           ),  # noqa
    ( 29, 'ru', 'No',           'Ялгаза'            ),  # noqa
    ( 30, 'en', 'No',           'Pereture'          ),  # noqa
    ( 30, 'ru', 'No',           'Перетур'           ),  # noqa
    ( 31, 'en', 'No',           'Yukas\' Earth'     ),  # noqa
    ( 31, 'ru', 'No',           'Земля Юкаса'       ),  # noqa
    ( 32, 'en', 'No',           'Pransh'            ),  # noqa
    ( 32, 'ru', 'No',           'Пранш'             ),  # noqa
    ( 33, 'en', 'No',           'Diamasy'           ),  # noqa
    ( 33, 'ru', 'No',           'Диамаси'           ),  # noqa
    ( 34, 'en', 'No',           'Cibarrack'         ),  # noqa
    ( 34, 'ru', 'No',           'Цыбаррак'          ),  # noqa
    ( 35, 'en', 'No',           'Gorgio'            ),  # noqa
    ( 35, 'ru', 'No',           'Жоржо'             ),  # noqa
    ( 36, 'en', 'No',           'Lanka Stratin'     ),  # noqa
    ( 36, 'ru', 'No',           'Ланка Стратин'     ),  # noqa
    ( 37, 'en', 'No',           'Neglyash'          ),  # noqa
    ( 37, 'ru', 'No',           'Негляш'            ),  # noqa
    ( 38, 'en', 'No',           'Likamuerte'        ),  # noqa
    ( 38, 'ru', 'No',           'Лайкамуэрте'       ),  # noqa
    ( 39, 'en', 'No',           'Eiya'              ),  # noqa
    ( 39, 'ru', 'No',           'Эйя'               ),  # noqa
    ( 40, 'en', 'No',           'Sujim'             ),  # noqa
    ( 40, 'ru', 'No',           'Суджим'            ),  # noqa
    ( 41, 'en', 'No',           'Barcag'            ),  # noqa
    ( 41, 'ru', 'No',           'Баркаг'            ),  # noqa
    ( 42, 'en', 'No',           'Agasly'            ),  # noqa
    ( 42, 'ru', 'No',           'Агасли'            ),  # noqa
    ( 43, 'en', 'No',           'Xarcimus'          ),  # noqa
    ( 43, 'ru', 'No',           'Ксарцимус'         ),  # noqa
    ( 44, 'en', 'No',           'Neosphene'         ),  # noqa
    ( 44, 'ru', 'No',           'Неосфена'          ),  # noqa
    ( 45, 'en', 'No',           'Hard Core'         ),  # noqa
    ( 45, 'ru', 'No',           'Хард Кор'          ),  # noqa
    ( 46, 'en', 'No',           'Sanctuary Kuchgun' ),  # noqa
    ( 46, 'ru', 'No',           'Заповедный Кучгун' ),  # noqa
    ( 47, 'en', 'No',           'Dipa'              ),  # noqa
    ( 47, 'ru', 'No',           'Дипа'              ),  # noqa
    ( 48, 'en', 'No',           'Moreys'            ),  # noqa
    ( 48, 'ru', 'No',           'Мурены'            ),  # noqa
    ( 49, 'en', 'No',           'Angia'             ),  # noqa
    ( 49, 'ru', 'No',           'Энжа'              ),  # noqa
    ( 50, 'en', 'No',           'Gashikh'           ),  # noqa
    ( 50, 'ru', 'No',           'Гаших'             ),  # noqa
    ( 51, 'en', 'No',           'Urragakh'          ),  # noqa
    ( 51, 'ru', 'No',           'Уррагах'           ),  # noqa
    ( 52, 'en', 'No',           'Menna Geacine'     ),  # noqa
    ( 52, 'ru', 'No',           'Менна Геацин'      ),  # noqa
    ( 53, 'en', 'No',           'Oshchily'          ),  # noqa
    ( 53, 'ru', 'No',           'Ощили'             ),  # noqa
    ( 54, 'en', 'No',           'Changa'            ),  # noqa
    ( 54, 'ru', 'No',           'Чанга'             ),  # noqa
    ( 55, 'en', 'No',           'Benthal Sand'      ),  # noqa
    ( 55, 'ru', 'No',           'Донный Песок'      ),  # noqa
    ( 56, 'en', 'No',           'Laika'             ),  # noqa
    ( 56, 'ru', 'No',           'Ляйка'             ),  # noqa
    ( 57, 'en', 'No',           'Muynus'            ),  # noqa
    ( 57, 'ru', 'No',           'Муйнус'            ),  # noqa
    ( 58, 'en', 'No',           'Fargadry'          ),  # noqa
    ( 58, 'ru', 'No',           'Фаргадры'          ),  # noqa
    ( 59, 'en', 'No',           'Panka Ailory'      ),  # noqa
    ( 59, 'ru', 'No',           'Панка Айлори'      ),  # noqa
    ( 60, 'en', 'No',           'Gnady'             ),  # noqa
    ( 60, 'ru', 'No',           'Гнады'             ),  # noqa
    ( 61, 'en', 'No',           'Zanma'             ),  # noqa
    ( 61, 'ru', 'No',           'Занма'             ),  # noqa
    ( 62, 'en', 'No',           'Einanala'          ),  # noqa
    ( 62, 'ru', 'No',           'Эйнанала'          ),  # noqa
    ( 63, 'en', 'No',           'Bek'               ),  # noqa
    ( 63, 'ru', 'No',           'Бек'               ),  # noqa
    ( 64, 'en', 'No',           'Alexania'          ),  # noqa
    ( 64, 'ru', 'No',           'Алексания'         ),  # noqa
    ( 65, 'en', 'No',           'Hukue'             ),  # noqa
    ( 65, 'ru', 'No',           'Хуку'              ),  # noqa
    ( 66, 'en', 'No',           'Listia'            ),  # noqa
    ( 66, 'ru', 'No',           'Листия'            ),  # noqa
    ( 67, 'en', 'No',           'Arta-lorag'        ),  # noqa
    ( 67, 'ru', 'No',           'Арта-лораг'        ),  # noqa
    ( 68, 'en', 'No',           'Hemezda'           ),  # noqa
    ( 68, 'ru', 'No',           'Гемезда'           ),  # noqa
    ( 69, 'en', 'No',           'Bonnasis'          ),  # noqa
    ( 69, 'ru', 'No',           'Боннасис'          ),  # noqa
    ( 70, 'en', 'No',           'Jublar'            ),  # noqa
    ( 70, 'ru', 'No',           'Юблар'             ),  # noqa
    ( 71, 'en', 'No',           'Zhenebe'           ),  # noqa
    ( 71, 'ru', 'No',           'Женеба'            ),  # noqa
    ( 72, 'en', 'No',           'Malior Carcass'    ),  # noqa
    ( 72, 'ru', 'No',           'Каракас Мальора'   ),  # noqa
    ( 73, 'en', 'No',           'Hell'              ),  # noqa
    ( 73, 'ru', 'No',           'Ад'                ),  # noqa
    ( 74, 'en', 'No',           'Heaven'            ),  # noqa
    ( 74, 'ru', 'No',           'Рай'               ),  # noqa
    ( 75, 'en', 'No',           'Limbo'             ),  # noqa
    ( 75, 'ru', 'No',           'Чистилище'         ),  # noqa
    ( 76, 'en', 'No',           'Duade'             ),  # noqa
    ( 76, 'ru', 'No',           'Дуада'             ),  # noqa
    ( 77, 'en', 'No',           'Stage'             ),  # noqa
    ( 77, 'ru', 'No',           'Перегон'           ),  # noqa
    ( 78, 'en', 'No',           'Glotcus'           ),  # noqa
    ( 78, 'ru', 'No',           'Глоткус'           ),  # noqa
    ( 79, 'en', 'No',           'Darzania'          ),  # noqa
    ( 79, 'ru', 'No',           'Дарзания'          ),  # noqa
    ( 80, 'en', 'No',           'Pretun'            ),  # noqa
    ( 80, 'ru', 'No',           'Претун'            ),  # noqa
    ( 81, 'en', 'No',           'Mokva'             ),  # noqa
    ( 81, 'ru', 'No',           'Моква'             ),  # noqa
    ( 82, 'en', 'No',           'Shun'              ),  # noqa
    ( 82, 'ru', 'No',           'Шун'               ),  # noqa
    ( 83, 'en', 'No',           'Dorris Kaga'       ),  # noqa
    ( 83, 'ru', 'No',           'Доррис Кага'       ),  # noqa
    ( 84, 'en', 'No',           'Ultiro'            ),  # noqa
    ( 84, 'ru', 'No',           'Ултиро'            ),  # noqa
    ( 85, 'en', 'No',           'Gorick'            ),  # noqa
    ( 85, 'ru', 'No',           'Горик'             ),  # noqa
    ( 86, 'en', 'No',           'Zhintibus'         ),  # noqa
    ( 86, 'ru', 'No',           'Жинтибус'          ),  # noqa
    ( 87, 'en', 'No',           'Savvala'           ),  # noqa
    ( 87, 'ru', 'No',           'Саввала'           ),  # noqa
    ( 88, 'en', 'No',           'Liry'              ),  # noqa
    ( 88, 'ru', 'No',           'Лири'              ),  # noqa
    ( 89, 'en', 'No',           'Urgue'             ),  # noqa
    ( 89, 'ru', 'No',           'Ургу'              ),  # noqa
    ( 90, 'en', 'No',           'Vestala'           ),  # noqa
    ( 90, 'ru', 'No',           'Вестала'           ),  # noqa
    ( 91, 'en', 'No',           'Dlory'             ),  # noqa
    ( 91, 'ru', 'No',           'Длори'             ),  # noqa
    ( 92, 'en', 'No',           'Bgasack'           ),  # noqa
    ( 92, 'ru', 'No',           'Бгасак'            ),  # noqa
    ( 93, 'en', 'No',           'Knout'             ),  # noqa
    ( 93, 'ru', 'No',           'Кнут'              ),  # noqa
    ( 94, 'en', 'No',           'Phinnirive'        ),  # noqa
    ( 94, 'ru', 'No',           'Финнириве'         ),  # noqa
    ( 95, 'en', 'No',           'Aiken Ma'          ),  # noqa
    ( 95, 'ru', 'No',           'Айкен Ма'          ),  # noqa
    ( 96, 'en', 'No',           'Horkhy'            ),  # noqa
    ( 96, 'ru', 'No',           'Хорхи'             ),  # noqa
    ( 97, 'en', 'No',           'Trannabash'        ),  # noqa
    ( 97, 'ru', 'No',           'Траннбаш'          ),  # noqa
    ( 98, 'en', 'No',           'Belishev Earth'    ),  # noqa
    ( 98, 'ru', 'No',           'Земля Белышева'    ),  # noqa
    ( 99, 'en', 'No',           'Unnamed'           ),  # noqa
    ( 99, 'ru', 'No',           'Безымянная'        ),  # noqa
    (100, 'en', 'No',           'Purkator'          ),  # noqa
    (100, 'ru', 'No',           'Пуркатор'          ),  # noqa
    (101, 'en', 'No',           'Mepla'             ),  # noqa
    (101, 'ru', 'No',           'Мепла'             ),  # noqa
    (102, 'en', 'No',           'Lyunkun'           ),  # noqa
    (102, 'ru', 'No',           'Люнкун'            ),  # noqa
    (103, 'en', 'No',           'Pustarga'          ),  # noqa
    (103, 'ru', 'No',           'Пустарга'          ),  # noqa
    (104, 'en', 'No',           'Bakhus'            ),  # noqa
    (104, 'ru', 'No',           'Баххус'            ),  # noqa
    (105, 'en', 'No',           'Sahanory'          ),  # noqa
    (105, 'ru', 'No',           'Саанори'           ),  # noqa
    (106, 'en', 'No',           'Zhistin'           ),  # noqa
    (106, 'ru', 'No',           'Жистин'            ),  # noqa
    (107, 'en', 'No',           'Azadagra'          ),  # noqa
    (107, 'ru', 'No',           'Азадагра'          ),  # noqa
    (108, 'en', 'No',           'Mercatory'         ),  # noqa
    (108, 'ru', 'No',           'Меркатори'         ),  # noqa
    (109, 'en', 'No',           'Pinna'             ),  # noqa
    (109, 'ru', 'No',           'Пинна'             ),  # noqa
    (110, 'en', 'No',           'Kamut'             ),  # noqa
    (110, 'ru', 'No',           'Камут'             ),  # noqa
    (111, 'en', 'No',           'Leine'             ),  # noqa
    (111, 'ru', 'No',           'Лейна'             ),  # noqa
    (112, 'en', 'No',           'Market'            ),  # noqa
    (112, 'ru', 'No',           'Базар'             ),  # noqa
    (113, 'en', 'No',           'Pressimo'          ),  # noqa
    (113, 'ru', 'No',           'Прессимо'          ),  # noqa
    (114, 'en', 'No',           'Raptis'            ),  # noqa
    (114, 'ru', 'No',           'Раптис'            ),  # noqa
    (115, 'en', 'No',           'Big Chimek'        ),  # noqa
    (115, 'ru', 'No',           'Большой Чимек'     ),  # noqa
    (116, 'en', 'No',           'Rice'              ),  # noqa
    (116, 'ru', 'No',           'Рис'               ),  # noqa
    (117, 'en', 'No',           'Leilash'           ),  # noqa
    (117, 'ru', 'No',           'Лайлаш'            ),  # noqa
    (118, 'en', 'No',           'Violet'            ),  # noqa
    (118, 'ru', 'No',           'Фиолет'            ),  # noqa
    (119, 'en', 'No',           'Brapkhor'          ),  # noqa
    (119, 'ru', 'No',           'Брапхор'           ),  # noqa
    (120, 'en', 'No',           'Khanaputra'        ),  # noqa
    (120, 'ru', 'No',           'Ханапутра'         ),  # noqa
    (121, 'en', 'No',           'Izginya'           ),  # noqa
    (121, 'ru', 'No',           'Изгинья'           ),  # noqa
    (122, 'en', 'No',           'Lekalos'           ),  # noqa
    (122, 'ru', 'No',           'Лекалос'           ),  # noqa
    (123, 'en', 'No',           'Donsh'             ),  # noqa
    (123, 'ru', 'No',           'Донш'              ),  # noqa
    (124, 'en', 'No',           'Rapakha'           ),  # noqa
    (124, 'ru', 'No',           'Рапаха'            ),  # noqa
    (125, 'en', 'No',           'Dewue Assory'      ),  # noqa
    (125, 'ru', 'No',           'Дэу Ассори'        ),  # noqa
    (126, 'en', 'No',           'Nuy'               ),  # noqa
    (126, 'ru', 'No',           'Нуи'               ),  # noqa
    (127, 'en', 'No',           'Veve'              ),  # noqa
    (127, 'ru', 'No',           'Вевы'              ),  # noqa
    (128, 'en', 'No',           'Tlalack'           ),  # noqa
    (128, 'ru', 'No',           'Тлалак'            ),  # noqa
    (129, 'en', 'No',           'Khottoshy'         ),  # noqa
    (129, 'ru', 'No',           'Хотташи'           ),  # noqa
    (130, 'en', 'No',           'Arnaul'            ),  # noqa
    (130, 'ru', 'No',           'Арнаул'            ),  # noqa
    (131, 'en', 'No',           'Dimezda'           ),  # noqa
    (131, 'ru', 'No',           'Димезда'           ),  # noqa
    (132, 'en', 'No',           'Ikka'              ),  # noqa
    (132, 'ru', 'No',           'Икка'              ),  # noqa
    (133, 'en', 'No',           'Russimet'          ),  # noqa
    (133, 'ru', 'No',           'Русимет'           ),  # noqa
    (134, 'en', 'No',           'Hakle'             ),  # noqa
    (134, 'ru', 'No',           'Хакл'              ),  # noqa
    (135, 'en', 'No',           'Chuiky'            ),  # noqa
    (135, 'ru', 'No',           'Чуйки'             ),  # noqa
    (136, 'en', 'No',           'Curl'              ),  # noqa
    (136, 'ru', 'No',           'Локон'             ),  # noqa
    (137, 'en', 'No',           'Punisse'           ),  # noqa
    (137, 'ru', 'No',           'Пунисе'            ),  # noqa
    (138, 'en', 'No',           'Dreador'           ),  # noqa
    (138, 'ru', 'No',           'Драдор'            ),  # noqa
    (139, 'en', 'No',           'Bashna'            ),  # noqa
    (139, 'ru', 'No',           'Башна'             ),  # noqa
    (140, 'en', 'No',           'Mess'              ),  # noqa
    (140, 'ru', 'No',           'Переплет'          ),  # noqa
    (141, 'en', 'No',           'Ibez'              ),  # noqa
    (141, 'ru', 'No',           'Ибез'              ),  # noqa
    (142, 'en', 'No',           'Uchkundin'         ),  # noqa
    (142, 'ru', 'No',           'Учкундин'          ),  # noqa
    (143, 'en', 'No',           'Kirshie'           ),  # noqa
    (143, 'ru', 'No',           'Керши'             ),  # noqa
    (144, 'en', 'No',           'Vinett'            ),  # noqa
    (144, 'ru', 'No',           'Винетт'            ),  # noqa
    (145, 'en', 'No',           'Cladis'            ),  # noqa
    (145, 'ru', 'No',           'Клэдис'            ),  # noqa
    (146, 'en', 'No',           'Betkh'             ),  # noqa
    (146, 'ru', 'No',           'Бетх'              ),  # noqa
    (147, 'en', 'No',           'Larlory'           ),  # noqa
    (147, 'ru', 'No',           'Ларлори'           ),  # noqa
    (148, 'en', 'No',           'Askasinash'        ),  # noqa
    (148, 'ru', 'No',           'Аскасинаш'         ),  # noqa
    (149, 'en', 'No',           'Zone'              ),  # noqa
    (149, 'ru', 'No',           'Зона'              ),  # noqa
    (150, 'en', 'No',           'Sussick'           ),  # noqa
    (150, 'ru', 'No',           'Суссик'            ),  # noqa
    (151, 'en', 'No',           'Diter'             ),  # noqa
    (151, 'ru', 'No',           'Дитер'             ),  # noqa
    (152, 'en', 'No',           'Robarra'           ),  # noqa
    (152, 'ru', 'No',           'Робарра'           ),  # noqa
    (153, 'en', 'No',           'Prusag'            ),  # noqa
    (153, 'ru', 'No',           'Прусаг'            ),  # noqa
    (154, 'en', 'No',           'Luminior'          ),  # noqa
    (154, 'ru', 'No',           'Люминиор'          ),  # noqa
    (155, 'en', 'No',           'Aven'              ),  # noqa
    (155, 'ru', 'No',           'Авен'              ),  # noqa
    (156, 'en', 'No',           'Klakla'            ),  # noqa
    (156, 'ru', 'No',           'Клакла'            ),  # noqa
    (157, 'en', 'No',           'Hugberids'         ),  # noqa
    (157, 'ru', 'No',           'Хубериды'          ),  # noqa
    (158, 'en', 'No',           'Dora'              ),  # noqa
    (158, 'ru', 'No',           'Дора'              ),  # noqa
    (159, 'en', 'No',           'Ezmeralda'         ),  # noqa
    (159, 'ru', 'No',           'Эзмеральда'        ),  # noqa
    (160, 'en', 'No',           'Pinky'             ),  # noqa
    (160, 'ru', 'No',           'Пинки'             ),  # noqa
    (161, 'en', 'No',           'Farevex'           ),  # noqa
    (161, 'ru', 'No',           'Ферфекс'           ),  # noqa
    (162, 'en', 'No',           'Bulba'             ),  # noqa
    (162, 'ru', 'No',           'Бульба'            ),  # noqa
    (163, 'en', 'No',           'Siamin'            ),  # noqa
    (163, 'ru', 'No',           'Сиамин'            ),  # noqa
    (164, 'en', 'No',           'Chelemsan'         ),  # noqa
    (164, 'ru', 'No',           'Челемсан'          ),  # noqa
    (165, 'en', 'No',           'Kinochy'           ),  # noqa
    (165, 'ru', 'No',           'Киноччи'           ),  # noqa
    (166, 'en', 'No',           'Seleue-dangan'     ),  # noqa
    (166, 'ru', 'No',           'Селеу-данган'      ),  # noqa
    (167, 'en', 'No',           'Ernedis'           ),  # noqa
    (167, 'ru', 'No',           'Эрнедис'           ),  # noqa
    (168, 'en', 'No',           'Pirrikaka'         ),  # noqa
    (168, 'ru', 'No',           'Пиррикака'         ),  # noqa
    (169, 'en', 'No',           'Suggar'            ),  # noqa
    (169, 'ru', 'No',           'Цуккар'            ),  # noqa
    (170, 'en', 'No',           'Ziraldack'         ),  # noqa
    (170, 'ru', 'No',           'Зиралдак'          ),  # noqa
    (171, 'en', 'No',           'Yazans'            ),  # noqa
    (171, 'ru', 'No',           'Язаны'             ),  # noqa
    (172, 'en', 'No',           'Lensin'            ),  # noqa
    (172, 'ru', 'No',           'Ленсин'            ),  # noqa
    (173, 'en', 'No',           'Shlagon'           ),  # noqa
    (173, 'ru', 'No',           'Шлагон'            ),  # noqa
    (174, 'en', 'No',           'Vampiury'          ),  # noqa
    (174, 'ru', 'No',           'Вапиури'           ),  # noqa
    (175, 'en', 'No',           'Lamkeng'           ),  # noqa
    (175, 'ru', 'No',           'Ламкенг'           ),  # noqa
    (176, 'en', 'No',           'Jadda'             ),  # noqa
    (176, 'ru', 'No',           'Джадда'            ),  # noqa
    (177, 'en', 'No',           'Sisyphus'          ),  # noqa
    (177, 'ru', 'No',           'Сизиф'             ),  # noqa
    (178, 'en', 'No',           'Eleonearch'        ),  # noqa
    (178, 'ru', 'No',           'Элеонеарх'         ),  # noqa
    (179, 'en', 'No',           'Cryptid'           ),  # noqa
    (179, 'ru', 'No',           'Криптид'           ),  # noqa
    (180, 'en', 'No',           'Susander'          ),  # noqa
    (180, 'ru', 'No',           'Сусандр'           ),  # noqa
    (181, 'en', 'No',           'Bunney'            ),  # noqa
    (181, 'ru', 'No',           'Бунней'            ),  # noqa
    (182, 'en', 'No',           'Blizzard'          ),  # noqa
    (182, 'ru', 'No',           'Вьюга'             ),  # noqa
    (183, 'en', 'No',           'Silesty'           ),  # noqa
    (183, 'ru', 'No',           'Силести'           ),  # noqa
    (184, 'en', 'No',           'Rippo'             ),  # noqa
    (184, 'ru', 'No',           'Риппо'             ),  # noqa
    (185, 'en', 'No',           'Alenga'            ),  # noqa
    (185, 'ru', 'No',           'Аленга'            ),  # noqa
    (186, 'en', 'No',           'Kyanma'            ),  # noqa
    (186, 'ru', 'No',           'Кьянма'            ),  # noqa
    (187, 'en', 'No',           'Paiball Drying'    ),  # noqa
    (187, 'ru', 'No',           'Сушка Пайбола'     ),  # noqa
    (188, 'en', 'No',           'Trashey'           ),  # noqa
    (188, 'ru', 'No',           'Трашея'            ),  # noqa
    (189, 'en', 'No',           'Dindare'           ),  # noqa
    (189, 'ru', 'No',           'Диндарэ'           ),  # noqa
    (190, 'en', 'No',           'Pelempey'          ),  # noqa
    (190, 'ru', 'No',           'Пелемпей'          ),  # noqa
    (191, 'en', 'No',           'Horch'             ),  # noqa
    (191, 'ru', 'No',           'Хорч'              ),  # noqa
    (192, 'en', 'No',           'Vangesh'           ),  # noqa
    (192, 'ru', 'No',           'Вангеш'            ),  # noqa
    (193, 'en', 'No',           'Dladiue'           ),  # noqa
    (193, 'ru', 'No',           'Дладиу'            ),  # noqa
    (194, 'en', 'No',           'Ire'               ),  # noqa
    (194, 'ru', 'No',           'Аэ'                ),  # noqa
    (195, 'en', 'No',           'Binnary'           ),  # noqa
    (195, 'ru', 'No',           'Биннари'           ),  # noqa
    (196, 'en', 'No',           'Diodar'            ),  # noqa
    (196, 'ru', 'No',           'Диодар'            ),  # noqa
    (197, 'en', 'No',           'Pernep'            ),  # noqa
    (197, 'ru', 'No',           'Пернеп'            ),  # noqa
    (198, 'en', 'No',           'Sharkhan'          ),  # noqa
    (198, 'ru', 'No',           'Шаркан'            ),  # noqa
    (199, 'en', 'No',           'Pritlo'            ),  # noqa
    (199, 'ru', 'No',           'Притло'            ),  # noqa
    (200, 'en', 'No',           'Dudau'             ),  # noqa
    (200, 'ru', 'No',           'Дудау'             ),  # noqa
    (201, 'en', 'No',           'Nenrit'            ),  # noqa
    (201, 'ru', 'No',           'Ненрит'            ),  # noqa
    (202, 'en', 'No',           'Eleoriaty'         ),  # noqa
    (202, 'ru', 'No',           'Элеориати'         ),  # noqa
    (203, 'en', 'No',           'Zekh'              ),  # noqa
    (203, 'ru', 'No',           'Зехх'              ),  # noqa
    (204, 'en', 'No',           'Smiryana'          ),  # noqa
    (204, 'ru', 'No',           'Смиряна'           ),  # noqa
    (205, 'en', 'No',           'Khukhrs'           ),  # noqa
    (205, 'ru', 'No',           'Хухры'             ),  # noqa
    (206, 'en', 'No',           'Eiga'              ),  # noqa
    (206, 'ru', 'No',           'Эйга'              ),  # noqa
    (207, 'en', 'No',           'Mansa-ukash'       ),  # noqa
    (207, 'ru', 'No',           'Манса-укаш'        ),  # noqa
    (208, 'en', 'No',           'Rinoa'             ),  # noqa
    (208, 'ru', 'No',           'Риноа'             ),  # noqa
    (209, 'en', 'No',           'Samma'             ),  # noqa
    (209, 'ru', 'No',           'Самма'             ),  # noqa
    (210, 'en', 'No',           'Bestis'            ),  # noqa
    (210, 'ru', 'No',           'Бестис'            ),  # noqa
    (211, 'en', 'No',           'Logant'            ),  # noqa
    (211, 'ru', 'No',           'Логант'            ),  # noqa
    (212, 'en', 'No',           'Kreonar'           ),  # noqa
    (212, 'ru', 'No',           'Креонар'           ),  # noqa
    (213, 'en', 'No',           'Tyulds'            ),  # noqa
    (213, 'ru', 'No',           'Тюлды'             ),  # noqa
    (214, 'en', 'No',           'Zimyash'           ),  # noqa
    (214, 'ru', 'No',           'Зимьяш'            ),  # noqa
    (215, 'en', 'No',           'Tzi Maripue'       ),  # noqa
    (215, 'ru', 'No',           'Цзы Марипу'        ),  # noqa
    (216, 'en', 'No',           'Kalkue'            ),  # noqa
    (216, 'ru', 'No',           'Калку'             ),  # noqa
    (217, 'en', 'No',           'Sanapol'           ),  # noqa
    (217, 'ru', 'No',           'Санаполь'          ),  # noqa
    (218, 'en', 'No',           'Bermelea'          ),  # noqa
    (218, 'ru', 'No',           'Бермелеа'          ),  # noqa
    (219, 'en', 'No',           'Arrol'             ),  # noqa
    (219, 'ru', 'No',           'Аррол'             ),  # noqa
    (220, 'en', 'No',           'Nanarue'           ),  # noqa
    (220, 'ru', 'No',           'Нанару'            ),  # noqa
    (221, 'en', 'No',           'Logiman'           ),  # noqa
    (221, 'ru', 'No',           'Ложиман'           ),  # noqa
    (222, 'en', 'No',           'Dnea-rangut'       ),  # noqa
    (222, 'ru', 'No',           'Днеа-рангут'       ),  # noqa
    (223, 'en', 'No',           'Banafarm'          ),  # noqa
    (223, 'ru', 'No',           'Банаферма'         ),  # noqa
    (224, 'en', 'No',           'Arie Flower'       ),  # noqa
    (224, 'ru', 'No',           'Цветок Ари'        ),  # noqa
    (225, 'en', 'No',           'Ashoka'            ),  # noqa
    (225, 'ru', 'No',           'Ашока'             ),  # noqa
    (226, 'en', 'No',           'Sizer'             ),  # noqa
    (226, 'ru', 'No',           'Сизюн'             ),  # noqa
    (227, 'en', 'No',           'Minislave'         ),  # noqa
    (227, 'ru', 'No',           'Минислав'          ),  # noqa
    (228, 'en', 'No',           'Hergedos'          ),  # noqa
    (228, 'ru', 'No',           'Гергедос'          ),  # noqa
    (229, 'en', 'No',           'Vaipra'            ),  # noqa
    (229, 'ru', 'No',           'Вайпра'            ),  # noqa
    (230, 'en', 'No',           'Neonal'            ),  # noqa
    (230, 'ru', 'No',           'Неонал'            ),  # noqa
    (231, 'en', 'No',           'Phander'           ),  # noqa
    (231, 'ru', 'No',           'Фандры'            ),  # noqa
    (232, 'en', 'No',           'Bespeday'          ),  # noqa
    (232, 'ru', 'No',           'Беспедей'          ),  # noqa
    (233, 'en', 'No',           'Umshun'            ),  # noqa
    (233, 'ru', 'No',           'Умчун'             ),  # noqa
    (234, 'en', 'No',           'Perenis'           ),  # noqa
    (234, 'ru', 'No',           'Перенис'           ),  # noqa
    (235, 'en', 'No',           'Ruptur'            ),  # noqa
    (235, 'ru', 'No',           'Руптур'            ),  # noqa
    (236, 'en', 'No',           'Xenophas'          ),  # noqa
    (236, 'ru', 'No',           'Ксенофас'          ),  # noqa
    (237, 'en', 'No',           'Herkhedy'          ),  # noqa
    (237, 'ru', 'No',           'Герхеды'           ),  # noqa
    (238, 'en', 'No',           'Lisnue'            ),  # noqa
    (238, 'ru', 'No',           'Лисну'             ),  # noqa
    (239, 'en', 'No',           'Rratis'            ),  # noqa
    (239, 'ru', 'No',           'Рратис'            ),  # noqa
    (240, 'en', 'No',           'Zezden'            ),  # noqa
    (240, 'ru', 'No',           'Зезден'            ),  # noqa
    (241, 'en', 'No',           'Valla Neo'         ),  # noqa
    (241, 'ru', 'No',           'Валла Нео'         ),  # noqa
    (242, 'en', 'No',           'Kent'              ),  # noqa
    (242, 'ru', 'No',           'Кент'              ),  # noqa
    (243, 'en', 'No',           'Ramphyne'          ),  # noqa
    (243, 'ru', 'No',           'Рамфина'           ),  # noqa
    (244, 'en', 'No',           'Neya'              ),  # noqa
    (244, 'ru', 'No',           'Нэйя'              ),  # noqa
    (245, 'en', 'No',           'Belliny'           ),  # noqa
    (245, 'ru', 'No',           'Беллини'           ),  # noqa
    (246, 'en', 'No',           'Purkhen'           ),  # noqa
    (246, 'ru', 'No',           'Пурхен'            ),  # noqa
    (247, 'en', 'No',           'Shiorie'           ),  # noqa
    (247, 'ru', 'No',           'Шиори'             ),  # noqa
    (248, 'en', 'No',           'Dnadzory'          ),  # noqa
    (248, 'ru', 'No',           'Днадзори'          ),  # noqa
    (249, 'en', 'No',           'Squadro'           ),  # noqa
    (249, 'ru', 'No',           'Скуадро'           ),  # noqa
    (250, 'en', 'No',           'Aplit'             ),  # noqa
    (250, 'ru', 'No',           'Аплит'             ),  # noqa
    (251, 'en', 'No',           'Nastis'            ),  # noqa
    (251, 'ru', 'No',           'Настис'            ),  # noqa
    (252, 'en', 'No',           'Zaigra'            ),  # noqa
    (252, 'ru', 'No',           'Заигра'            ),  # noqa
    (253, 'en', 'No',           'Vantra Molka'      ),  # noqa
    (253, 'ru', 'No',           'Вантра Молка'      ),  # noqa
    (254, 'en', 'No',           'Peristidue'        ),  # noqa
    (254, 'ru', 'No',           'Перистиду'         ),  # noqa
    (255, 'en', 'No',           'Lumpa David'       ),  # noqa
    (255, 'ru', 'No',           'Лумпа Дэвид'       ),  # noqa
    (256, 'en', 'No',           'Tzulols'           ),  # noqa
    (256, 'ru', 'No',           'Цулолы'            ),  # noqa
    (257, 'en', 'No',           'Yakhchar'          ),  # noqa
    (257, 'ru', 'No',           'Яхчар'             ),  # noqa
    (258, 'en', 'No',           'Meniue'            ),  # noqa
    (258, 'ru', 'No',           'Мениу'             ),  # noqa
    (259, 'en', 'No',           'Onela'             ),  # noqa
    (259, 'ru', 'No',           'Онела'             ),  # noqa
    (260, 'en', 'No',           'Majorbeck'         ),  # noqa
    (260, 'ru', 'No',           'Майорбек'          ),  # noqa
    (261, 'en', 'No',           'Plistine'          ),  # noqa
    (261, 'ru', 'No',           'Плистин'           ),  # noqa
    (262, 'en', 'No',           'Hyde'              ),  # noqa
    (262, 'ru', 'No',           'Гайда'             ),  # noqa
    (263, 'en', 'No',           'Sharkhalla'        ),  # noqa
    (263, 'ru', 'No',           'Шархалла'          ),  # noqa
    (264, 'en', 'No',           'Murps'             ),  # noqa
    (264, 'ru', 'No',           'Мурпс'             ),  # noqa
    (265, 'en', 'No',           'Phobia'            ),  # noqa
    (265, 'ru', 'No',           'Фобий'             ),  # noqa
    (266, 'en', 'No',           'Barbados'          ),  # noqa
    (266, 'ru', 'No',           'Барбадос'          ),  # noqa
    (267, 'en', 'No',           'Murineck'          ),  # noqa
    (267, 'ru', 'No',           'Муринека'          ),  # noqa
    (268, 'en', 'No',           'Hun'               ),  # noqa
    (268, 'ru', 'No',           'Гунн'              ),  # noqa
    (269, 'en', 'No',           'Zhdana'            ),  # noqa
    (269, 'ru', 'No',           'Ждана'             ),  # noqa
    (270, 'en', 'No',           'Sillis Old'        ),  # noqa
    (270, 'ru', 'No',           'Силлис Олд'        ),  # noqa
    (271, 'en', 'No',           'Vanasue'           ),  # noqa
    (271, 'ru', 'No',           'Ванасу'            ),  # noqa
    (272, 'en', 'No',           'Ut Barra'          ),  # noqa
    (272, 'ru', 'No',           'Ють Барра'         ),  # noqa
    (273, 'en', 'No',           'Pherpsykhene'      ),  # noqa
    (273, 'ru', 'No',           'Ферпсихена'        ),  # noqa
    (274, 'en', 'No',           'Zanter'            ),  # noqa
    (274, 'ru', 'No',           'Зантр'             ),  # noqa
    (275, 'en', 'No',           'Shesha Muneka'     ),  # noqa
    (275, 'ru', 'No',           'Шеша Мунека'       ),  # noqa
    (276, 'en', 'No',           'Canay'             ),  # noqa
    (276, 'ru', 'No',           'Канай'             ),  # noqa
    (277, 'en', 'No',           'Alevcap'           ),  # noqa
    (277, 'ru', 'No',           'Алевкап'           ),  # noqa
    (278, 'en', 'No',           'Zhitnin'           ),  # noqa
    (278, 'ru', 'No',           'Житнин'            ),  # noqa
    (279, 'en', 'No',           'Bach'              ),  # noqa
    (279, 'ru', 'No',           'Бах'               ),  # noqa
    (280, 'en', 'No',           'Vinifritis'        ),  # noqa
    (280, 'ru', 'No',           'Винифрит'          ),  # noqa
    (281, 'en', 'No',           'Kalls'             ),  # noqa
    (281, 'ru', 'No',           'Каллы'             ),  # noqa
    (282, 'en', 'No',           'Arghemma'          ),  # noqa
    (282, 'ru', 'No',           'Аргемма'           ),  # noqa
    (283, 'en', 'No',           'Lito'              ),  # noqa
    (283, 'ru', 'No',           'Лито'              ),  # noqa
    (284, 'en', 'No',           'Semune'            ),  # noqa
    (284, 'ru', 'No',           'Семуна'            ),  # noqa
    (285, 'en', 'No',           'Perostitus'        ),  # noqa
    (285, 'ru', 'No',           'Перостит'          ),  # noqa
    (286, 'en', 'No',           'Denky'             ),  # noqa
    (286, 'ru', 'No',           'Денки'             ),  # noqa
    (287, 'en', 'No',           'Cancus'            ),  # noqa
    (287, 'ru', 'No',           'Канкус'            ),  # noqa
    (288, 'en', 'No',           'Pireneus'          ),  # noqa
    (288, 'ru', 'No',           'Пиреней'           ),  # noqa
    (289, 'en', 'No',           'Ullacha'           ),  # noqa
    (289, 'ru', 'No',           'Уллача'            ),  # noqa
    (290, 'en', 'No',           'Egenory'           ),  # noqa
    (290, 'ru', 'No',           'Эженори'           ),  # noqa
    (291, 'en', 'No',           'Diastra'           ),  # noqa
    (291, 'ru', 'No',           'Диастра'           ),  # noqa
    (292, 'en', 'No',           'Irsa'              ),  # noqa
    (292, 'ru', 'No',           'Ирса'              ),  # noqa
    (293, 'en', 'No',           'Kentra'            ),  # noqa
    (293, 'ru', 'No',           'Кентра'            ),  # noqa
    (294, 'en', 'No',           'Shinakhernad'      ),  # noqa
    (294, 'ru', 'No',           'Шинахарнад'        ),  # noqa
    (295, 'en', 'No',           'Benesey'           ),  # noqa
    (295, 'ru', 'No',           'Бенесеи'           ),  # noqa
    (296, 'en', 'No',           'Vallid'            ),  # noqa
    (296, 'ru', 'No',           'Валлид'            ),  # noqa
    (297, 'en', 'No',           'Secundus Brald'    ),  # noqa
    (297, 'ru', 'No',           'Секундус Бралд'    ),  # noqa
    (298, 'en', 'No',           'Ploshch'           ),  # noqa
    (298, 'ru', 'No',           'Площ'              ),  # noqa
    (299, 'en', 'No',           'Sicotta'           ),  # noqa
    (299, 'ru', 'No',           'Сикотта'           ),  # noqa
    (300, 'en', 'No',           'Leana-mie'         ),  # noqa
    (300, 'ru', 'No',           'Леана-мие'         ),  # noqa
    (  1, 'en', 'Peleng',       'Shukheo'           ),  # noqa
    (  1, 'ru', 'Peleng',       'Шухэо'             ),  # noqa
    (  2, 'en', 'Peleng',       'Rakhish'           ),  # noqa
    (  2, 'ru', 'Peleng',       'Рахиш'             ),  # noqa
    (  3, 'en', 'Peleng',       'Gitzkaz'           ),  # noqa
    (  3, 'ru', 'Peleng',       'Джыцказ'           ),  # noqa
    (  4, 'en', 'Peleng',       'Rkheshlikh'        ),  # noqa
    (  4, 'ru', 'Peleng',       'Рехешлих'          ),  # noqa
    (  5, 'en', 'Peleng',       'Rokrenkha'         ),  # noqa
    (  5, 'ru', 'Peleng',       'Рокренха'          ),  # noqa
    (  6, 'en', 'Peleng',       'Krining'           ),  # noqa
    (  6, 'ru', 'Peleng',       'Крынинг'           ),  # noqa
    (  7, 'en', 'Peleng',       'Teudorkh'          ),  # noqa
    (  7, 'ru', 'Peleng',       'Тэудорх'           ),  # noqa
    (  8, 'en', 'Peleng',       'Shorgharotz'       ),  # noqa
    (  8, 'ru', 'Peleng',       'Шоргароц'          ),  # noqa
    (  9, 'en', 'Peleng',       'Geshy'             ),  # noqa
    (  9, 'ru', 'Peleng',       'Гешши'             ),  # noqa
    ( 10, 'en', 'Peleng',       'Tziptza'           ),  # noqa
    ( 10, 'ru', 'Peleng',       'Ципца'             ),  # noqa
    ( 11, 'en', 'Peleng',       'Zuyagil'           ),  # noqa
    ( 11, 'ru', 'Peleng',       'Зуягил'            ),  # noqa
    ( 12, 'en', 'Peleng',       'Gemikh'            ),  # noqa
    ( 12, 'ru', 'Peleng',       'Джемих'            ),  # noqa
    ( 13, 'en', 'Peleng',       'Silitz'            ),  # noqa
    ( 13, 'ru', 'Peleng',       'Силиц'             ),  # noqa
    ( 14, 'en', 'Peleng',       'Ragtz'             ),  # noqa
    ( 14, 'ru', 'Peleng',       'Рагц'              ),  # noqa
    ( 15, 'en', 'Peleng',       'Urnikh'            ),  # noqa
    ( 15, 'ru', 'Peleng',       'Урних'             ),  # noqa
    ( 16, 'en', 'Peleng',       'Pitue'             ),  # noqa
    ( 16, 'ru', 'Peleng',       'Питу'              ),  # noqa
    ( 17, 'en', 'Peleng',       'Bokalatz'          ),  # noqa
    ( 17, 'ru', 'Peleng',       'Бокалац'           ),  # noqa
    ( 18, 'en', 'Peleng',       'Shesha'            ),  # noqa
    ( 18, 'ru', 'Peleng',       'Шеша'              ),  # noqa
    ( 19, 'en', 'Peleng',       'Kayakha'           ),  # noqa
    ( 19, 'ru', 'Peleng',       'Каияха'            ),  # noqa
    ( 20, 'en', 'Peleng',       'Shchimea'          ),  # noqa
    ( 20, 'ru', 'Peleng',       'Щимеа'             ),  # noqa
    ( 21, 'en', 'Peleng',       'Zkhot'             ),  # noqa
    ( 21, 'ru', 'Peleng',       'Зхот'              ),  # noqa
    ( 22, 'en', 'Peleng',       'Dabozoe'           ),  # noqa
    ( 22, 'ru', 'Peleng',       'Дабозо'            ),  # noqa
    ( 23, 'en', 'Peleng',       'Garging'           ),  # noqa
    ( 23, 'ru', 'Peleng',       'Гаргынг'           ),  # noqa
    ( 24, 'en', 'Peleng',       'Chshasha'          ),  # noqa
    ( 24, 'ru', 'Peleng',       'Чшаша'             ),  # noqa
    ( 25, 'en', 'Peleng',       'Alkhatzing'        ),  # noqa
    ( 25, 'ru', 'Peleng',       'Алхацинг'          ),  # noqa
    ( 26, 'en', 'Peleng',       'Kheinkharona'      ),  # noqa
    ( 26, 'ru', 'Peleng',       'Хейнхарона'        ),  # noqa
    ( 27, 'en', 'Peleng',       'Pang'              ),  # noqa
    ( 27, 'ru', 'Peleng',       'Панг'              ),  # noqa
    ( 28, 'en', 'Peleng',       'Gazhmy'            ),  # noqa
    ( 28, 'ru', 'Peleng',       'Гэжми'             ),  # noqa
    ( 29, 'en', 'Peleng',       'Valuykh'           ),  # noqa
    ( 29, 'ru', 'Peleng',       'Валуйх'            ),  # noqa
    ( 30, 'en', 'Peleng',       'Phichin'           ),  # noqa
    ( 30, 'ru', 'Peleng',       'Фычин'             ),  # noqa
    ( 31, 'en', 'Peleng',       'Gramtzy'           ),  # noqa
    ( 31, 'ru', 'Peleng',       'Грамцы'            ),  # noqa
    ( 32, 'en', 'Peleng',       'Yokhang'           ),  # noqa
    ( 32, 'ru', 'Peleng',       'Иоханг'            ),  # noqa
    ( 33, 'en', 'Peleng',       'Erkhenamat'        ),  # noqa
    ( 33, 'ru', 'Peleng',       'Эрхенамат'         ),  # noqa
    ( 34, 'en', 'Peleng',       'Siyazzh'           ),  # noqa
    ( 34, 'ru', 'Peleng',       'Сиязж'             ),  # noqa
    ( 35, 'en', 'Peleng',       'Rakharogog'        ),  # noqa
    ( 35, 'ru', 'Peleng',       'Ракхарагог'        ),  # noqa
    ( 36, 'en', 'Peleng',       'Presyan'           ),  # noqa
    ( 36, 'ru', 'Peleng',       'Пресьян'           ),  # noqa
    ( 37, 'en', 'Peleng',       'Liyunta'           ),  # noqa
    ( 37, 'ru', 'Peleng',       'Лиюнта'            ),  # noqa
    ( 38, 'en', 'Peleng',       'Rshanikh'          ),  # noqa
    ( 38, 'ru', 'Peleng',       'Ршаних'            ),  # noqa
    ( 39, 'en', 'Peleng',       'Apeng'             ),  # noqa
    ( 39, 'ru', 'Peleng',       'Апенг'             ),  # noqa
    ( 40, 'en', 'Peleng',       'Zimer'             ),  # noqa
    ( 40, 'ru', 'Peleng',       'Зимер'             ),  # noqa
    ( 41, 'en', 'Peleng',       'Upkanta'           ),  # noqa
    ( 41, 'ru', 'Peleng',       'Упканта'           ),  # noqa
    ( 42, 'en', 'Peleng',       'Chichshasa'        ),  # noqa
    ( 42, 'ru', 'Peleng',       'Чичшаса'           ),  # noqa
    ( 43, 'en', 'Peleng',       'Deztzy'            ),  # noqa
    ( 43, 'ru', 'Peleng',       'Дэзци'             ),  # noqa
    ( 44, 'en', 'Peleng',       'Gogetzin'          ),  # noqa
    ( 44, 'ru', 'Peleng',       'Гогецин'           ),  # noqa
    ( 45, 'en', 'Peleng',       'Ulfengikh'         ),  # noqa
    ( 45, 'ru', 'Peleng',       'Улфенгих'          ),  # noqa
    ( 46, 'en', 'Peleng',       'Gishling'          ),  # noqa
    ( 46, 'ru', 'Peleng',       'Гишлинг'           ),  # noqa
    ( 47, 'en', 'Peleng',       'Dotzakhur'         ),  # noqa
    ( 47, 'ru', 'Peleng',       'Доцакхур'          ),  # noqa
    ( 48, 'en', 'Peleng',       'Eukhprakh'         ),  # noqa
    ( 48, 'ru', 'Peleng',       'Эухпрах'           ),  # noqa
    ( 49, 'en', 'Peleng',       'Umargatzin'        ),  # noqa
    ( 49, 'ru', 'Peleng',       'Умаргацин'         ),  # noqa
    ( 50, 'en', 'Peleng',       'Khing'             ),  # noqa
    ( 50, 'ru', 'Peleng',       'Хынг'              ),  # noqa
    ( 51, 'en', 'Peleng',       'Ching'             ),  # noqa
    ( 51, 'ru', 'Peleng',       'Чинг'              ),  # noqa
    ( 52, 'en', 'Peleng',       'Pkhayakha'         ),  # noqa
    ( 52, 'ru', 'Peleng',       'Пхаяха'            ),  # noqa
    ( 53, 'en', 'Peleng',       'Sujkhisa'          ),  # noqa
    ( 53, 'ru', 'Peleng',       'Суйхиса'           ),  # noqa
    ( 54, 'en', 'Peleng',       'Echikhmek'         ),  # noqa
    ( 54, 'ru', 'Peleng',       'Эчихмек'           ),  # noqa
    ( 55, 'en', 'Peleng',       'Nutzbasha'         ),  # noqa
    ( 55, 'ru', 'Peleng',       'Нуцбаша'           ),  # noqa
    ( 56, 'en', 'Peleng',       'Lenshikh'          ),  # noqa
    ( 56, 'ru', 'Peleng',       'Ленших'            ),  # noqa
    ( 57, 'en', 'Peleng',       'Ashjampa'          ),  # noqa
    ( 57, 'ru', 'Peleng',       'Ашьямпа'           ),  # noqa
    ( 58, 'en', 'Peleng',       'Ragaikh'           ),  # noqa
    ( 58, 'ru', 'Peleng',       'Рагайх'            ),  # noqa
    ( 59, 'en', 'Peleng',       'Gujkhinang'        ),  # noqa
    ( 59, 'ru', 'Peleng',       'Гуйхинанг'         ),  # noqa
    ( 60, 'en', 'Peleng',       'Titishapha'        ),  # noqa
    ( 60, 'ru', 'Peleng',       'Титичафа'          ),  # noqa
    ( 61, 'en', 'Peleng',       'Lekhaikha'         ),  # noqa
    ( 61, 'ru', 'Peleng',       'Лехайха'           ),  # noqa
    ( 62, 'en', 'Peleng',       'Zhalta'            ),  # noqa
    ( 62, 'ru', 'Peleng',       'Жалта'             ),  # noqa
    ( 63, 'en', 'Peleng',       'Shchirashka'       ),  # noqa
    ( 63, 'ru', 'Peleng',       'Щирашка'           ),  # noqa
    ( 64, 'en', 'Peleng',       'Zhanshema'         ),  # noqa
    ( 64, 'ru', 'Peleng',       'Жаншема'           ),  # noqa
    ( 65, 'en', 'Peleng',       'Gargatzig'         ),  # noqa
    ( 65, 'ru', 'Peleng',       'Гаргациг'          ),  # noqa
    ( 66, 'en', 'Peleng',       'Dranachy'          ),  # noqa
    ( 66, 'ru', 'Peleng',       'Драначчи'          ),  # noqa
    ( 67, 'en', 'Peleng',       'Keika'             ),  # noqa
    ( 67, 'ru', 'Peleng',       'Кейка'             ),  # noqa
    ( 68, 'en', 'Peleng',       'Radatzuy'          ),  # noqa
    ( 68, 'ru', 'Peleng',       'Радацуй'           ),  # noqa
    ( 69, 'en', 'Peleng',       'Bikhkena'          ),  # noqa
    ( 69, 'ru', 'Peleng',       'Бихкена'           ),  # noqa
    ( 70, 'en', 'Peleng',       'Liyantag'          ),  # noqa
    ( 70, 'ru', 'Peleng',       'Лиянтаг'           ),  # noqa
    (  1, 'en', 'People',       'Unix'              ),  # noqa
    (  1, 'ru', 'People',       'Юникс'             ),  # noqa
    (  2, 'en', 'People',       'Arania'            ),  # noqa
    (  2, 'ru', 'People',       'Эрания'            ),  # noqa
    (  3, 'en', 'People',       'Axelman'           ),  # noqa
    (  3, 'ru', 'People',       'Аксельман'         ),  # noqa
    (  4, 'en', 'People',       'Beta-ionis'        ),  # noqa
    (  4, 'ru', 'People',       'Бета-ионис'        ),  # noqa
    (  5, 'en', 'People',       'Kalagan'           ),  # noqa
    (  5, 'ru', 'People',       'Калаган'           ),  # noqa
    (  6, 'en', 'People',       'Linux'             ),  # noqa
    (  6, 'ru', 'People',       'Линукс'            ),  # noqa
    (  7, 'en', 'People',       'Shot'              ),  # noqa
    (  7, 'ru', 'People',       'Стопка'            ),  # noqa
    (  8, 'en', 'People',       'Zaporozhets'       ),  # noqa
    (  8, 'ru', 'People',       'Запорожец'         ),  # noqa
    (  9, 'en', 'People',       'Hullgalla'         ),  # noqa
    (  9, 'ru', 'People',       'Халгалла'          ),  # noqa
    ( 10, 'en', 'People',       'Astron'            ),  # noqa
    ( 10, 'ru', 'People',       'Астрон'            ),  # noqa
    ( 11, 'en', 'People',       'Elinia'            ),  # noqa
    ( 11, 'ru', 'People',       'Элиния'            ),  # noqa
    ( 12, 'en', 'People',       'Big Cauldron'      ),  # noqa
    ( 12, 'ru', 'People',       'Большой котел'     ),  # noqa
    ( 13, 'en', 'People',       'Heracle Finger'    ),  # noqa
    ( 13, 'ru', 'People',       'Палец Геракла'     ),  # noqa
    ( 14, 'en', 'People',       'Santa Barbara'     ),  # noqa
    ( 14, 'ru', 'People',       'Святая Барбара'    ),  # noqa
    ( 15, 'en', 'People',       'Incara'            ),  # noqa
    ( 15, 'ru', 'People',       'Инкара'            ),  # noqa
    ( 16, 'en', 'People',       'Malis Calanka'     ),  # noqa
    ( 16, 'ru', 'People',       'Малис Каланка'     ),  # noqa
    ( 17, 'en', 'People',       'Glove'             ),  # noqa
    ( 17, 'ru', 'People',       'Перчатка'          ),  # noqa
    ( 18, 'en', 'People',       'New Thiva'         ),  # noqa
    ( 18, 'ru', 'People',       'Новые Фивы'        ),  # noqa
    ( 19, 'en', 'People',       'Orlenon'           ),  # noqa
    ( 19, 'ru', 'People',       'Орленон'           ),  # noqa
    ( 20, 'en', 'People',       'Uppsala-Vega'      ),  # noqa
    ( 20, 'ru', 'People',       'Упсала-вега'       ),  # noqa
    ( 21, 'en', 'People',       'Axle'              ),  # noqa
    ( 21, 'ru', 'People',       'Полуось'           ),  # noqa
    ( 22, 'en', 'People',       'Dassilon'          ),  # noqa
    ( 22, 'ru', 'People',       'Дассилон'          ),  # noqa
    ( 23, 'en', 'People',       'Unasis'            ),  # noqa
    ( 23, 'ru', 'People',       'Юнасис'            ),  # noqa
    ( 24, 'en', 'People',       'Persephone'        ),  # noqa
    ( 24, 'ru', 'People',       'Персефона'         ),  # noqa
    ( 25, 'en', 'People',       'Prokrut'           ),  # noqa
    ( 25, 'ru', 'People',       'Прокрут'           ),  # noqa
    ( 26, 'en', 'People',       'Hope'              ),  # noqa
    ( 26, 'ru', 'People',       'Надежда'           ),  # noqa
    ( 27, 'en', 'People',       'Plinius'           ),  # noqa
    ( 27, 'ru', 'People',       'Плиний'            ),  # noqa
    ( 28, 'en', 'People',       'Capablanca'        ),  # noqa
    ( 28, 'ru', 'People',       'Капабланка'        ),  # noqa
    ( 29, 'en', 'People',       'Hanukah'           ),  # noqa
    ( 29, 'ru', 'People',       'Еврейский дом'     ),  # noqa
    ( 30, 'en', 'People',       'Uliss Port'        ),  # noqa
    ( 30, 'ru', 'People',       'Порт Улисс'        ),  # noqa
    ( 31, 'en', 'People',       'Grunwald'          ),  # noqa
    ( 31, 'ru', 'People',       'Грюнвальд'         ),  # noqa
    ( 32, 'en', 'People',       'Small Arthur'      ),  # noqa
    ( 32, 'ru', 'People',       'Малый Артур'       ),  # noqa
    ( 33, 'en', 'People',       'Windows'           ),  # noqa
    ( 33, 'ru', 'People',       'Окошки'            ),  # noqa
    ( 34, 'en', 'People',       'Simbimella'        ),  # noqa
    ( 34, 'ru', 'People',       'Симбимелла'        ),  # noqa
    ( 35, 'en', 'People',       'Lamaila'           ),  # noqa
    ( 35, 'ru', 'People',       'Ламайла'           ),  # noqa
    ( 36, 'en', 'People',       'Nesting Doll'      ),  # noqa
    ( 36, 'ru', 'People',       'Матрешка'          ),  # noqa
    ( 37, 'en', 'People',       'Alumina'           ),  # noqa
    ( 37, 'ru', 'People',       'Глинозем'          ),  # noqa
    ( 38, 'en', 'People',       'Crosses'           ),  # noqa
    ( 38, 'ru', 'People',       'Кресты'            ),  # noqa
    ( 39, 'en', 'People',       'Aurelius'          ),  # noqa
    ( 39, 'ru', 'People',       'Аурелий'           ),  # noqa
    ( 40, 'en', 'People',       'Neolangoria'       ),  # noqa
    ( 40, 'ru', 'People',       'Неолангория'       ),  # noqa
    ( 41, 'en', 'People',       'Kamenkov'          ),  # noqa
    ( 41, 'ru', 'People',       'Каменков'          ),  # noqa
    ( 42, 'en', 'People',       'Sybill'            ),  # noqa
    ( 42, 'ru', 'People',       'Сибил'             ),  # noqa
    ( 43, 'en', 'People',       'Raintrop'          ),  # noqa
    ( 43, 'ru', 'People',       'Райнтроп'          ),  # noqa
    ( 44, 'en', 'People',       'Aqualgon'          ),  # noqa
    ( 44, 'ru', 'People',       'Аквалгон'          ),  # noqa
    ( 45, 'en', 'People',       'Selivan'           ),  # noqa
    ( 45, 'ru', 'People',       'Селиван'           ),  # noqa
    ( 46, 'en', 'People',       'Grand Concorde'    ),  # noqa
    ( 46, 'ru', 'People',       'Гранд Конкорд'     ),  # noqa
    ( 47, 'en', 'People',       'Lorena'            ),  # noqa
    ( 47, 'ru', 'People',       'Лорена'            ),  # noqa
    ( 48, 'en', 'People',       'Rossiyanochka'     ),  # noqa
    ( 48, 'ru', 'People',       'Россияночка'       ),  # noqa
    ( 49, 'en', 'People',       'Pont'              ),  # noqa
    ( 49, 'ru', 'People',       'Понт'              ),  # noqa
    ( 50, 'en', 'People',       'Qurdania'          ),  # noqa
    ( 50, 'ru', 'People',       'Курдания'          ),  # noqa
    ( 51, 'en', 'People',       'Lixan Land'        ),  # noqa
    ( 51, 'ru', 'People',       'Земля Ликсана'     ),  # noqa
    ( 52, 'en', 'People',       'Velecia'           ),  # noqa
    ( 52, 'ru', 'People',       'Велеция'           ),  # noqa
    ( 53, 'en', 'People',       'Utzar'             ),  # noqa
    ( 53, 'ru', 'People',       'Уцар'              ),  # noqa
    ( 54, 'en', 'People',       'Kerala Park'       ),  # noqa
    ( 54, 'ru', 'People',       'Парк Керала'       ),  # noqa
    ( 55, 'en', 'People',       'Agora'             ),  # noqa
    ( 55, 'ru', 'People',       'Агора'             ),  # noqa
    ( 56, 'en', 'People',       'Contemptis'        ),  # noqa
    ( 56, 'ru', 'People',       'Контемптис'        ),  # noqa
    ( 57, 'en', 'People',       'Leyra'             ),  # noqa
    ( 57, 'ru', 'People',       'Лейра'             ),  # noqa
    ( 58, 'en', 'People',       'Vinitron'          ),  # noqa
    ( 58, 'ru', 'People',       'Винитрон'          ),  # noqa
    ( 59, 'en', 'People',       'Budana'            ),  # noqa
    ( 59, 'ru', 'People',       'Будана'            ),  # noqa
    ( 60, 'en', 'People',       'Corriolli'         ),  # noqa
    ( 60, 'ru', 'People',       'Корриоли'          ),  # noqa
    ( 61, 'en', 'People',       'Chakus'            ),  # noqa
    ( 61, 'ru', 'People',       'Чакус'             ),  # noqa
    ( 62, 'en', 'People',       'Bygal'             ),  # noqa
    ( 62, 'ru', 'People',       'Байгал'            ),  # noqa
    ( 63, 'en', 'People',       'Big Barrier'       ),  # noqa
    ( 63, 'ru', 'People',       'Большой Барьер'    ),  # noqa
    ( 64, 'en', 'People',       'Small Barrier'     ),  # noqa
    ( 64, 'ru', 'People',       'Малый Барьер'      ),  # noqa
    ( 65, 'en', 'People',       'Leskana'           ),  # noqa
    ( 65, 'ru', 'People',       'Лескана'           ),  # noqa
    ( 66, 'en', 'People',       'Jasper'            ),  # noqa
    ( 66, 'ru', 'People',       'Яшма'              ),  # noqa
    ( 67, 'en', 'People',       'Dora Present'      ),  # noqa
    ( 67, 'ru', 'People',       'Дора Презент'      ),  # noqa
    ( 68, 'en', 'People',       'Pint'              ),  # noqa
    ( 68, 'ru', 'People',       'Пинта'             ),  # noqa
    ( 69, 'en', 'People',       'Jullis'            ),  # noqa
    ( 69, 'ru', 'People',       'Юллис'             ),  # noqa
    ( 70, 'en', 'People',       'Intagon'           ),  # noqa
    ( 70, 'ru', 'People',       'Интагон'           ),  # noqa
    (  1, 'en', 'PirateClan',   'Rogeria'           ),  # noqa
    (  1, 'ru', 'PirateClan',   'Роджерия'          ),  # noqa
    (  2, 'en', 'PirateClan',   'Monovar'           ),  # noqa
    (  2, 'ru', 'PirateClan',   'Моновар'           ),  # noqa
    (  3, 'en', 'PirateClan',   'Schooner'          ),  # noqa
    (  3, 'ru', 'PirateClan',   'Шхуна'             ),  # noqa
    (  4, 'en', 'PirateClan',   'Pearl'             ),  # noqa
    (  4, 'ru', 'PirateClan',   'Жемчужина'         ),  # noqa
    (  5, 'en', 'PirateClan',   'Fale-de-Fae'       ),  # noqa
    (  5, 'ru', 'PirateClan',   'Фале-де-Фей'       ),  # noqa
    (  6, 'en', 'PirateClan',   'Gaaleon'           ),  # noqa
    (  6, 'ru', 'PirateClan',   'Гаалеон'           ),  # noqa
    (  0, 'en', 'Solar',        'Mercury'           ),  # noqa
    (  0, 'ru', 'Solar',        'Меркурий'          ),  # noqa
    (  1, 'en', 'Solar',        'Venus'             ),  # noqa
    (  1, 'ru', 'Solar',        'Венера'            ),  # noqa
    (  2, 'en', 'Solar',        'Earth'             ),  # noqa
    (  2, 'ru', 'Solar',        'Земля'             ),  # noqa
    (  3, 'en', 'Solar',        'Mars'              ),  # noqa
    (  3, 'ru', 'Solar',        'Марс'              ),  # noqa
    (  4, 'en', 'Solar',        'Jupiter'           ),  # noqa
    (  4, 'ru', 'Solar',        'Юпитер'            ),  # noqa
    (  5, 'en', 'Solar',        'Saturn'            ),  # noqa
    (  5, 'ru', 'Solar',        'Сатурн'            ),  # noqa
    (  6, 'en', 'Solar',        'Neptune'           ),  # noqa
    (  6, 'ru', 'Solar',        'Нептун'            ),  # noqa
    (  7, 'en', 'Solar',        'Uranus'            ),  # noqa
    (  7, 'ru', 'Solar',        'Уран'              ),  # noqa
    (  8, 'en', 'Solar',        'Pluto'             ),  # noqa
    (  8, 'ru', 'Solar',        'Плутон'            ),  # noqa
]
# @formatter:on


# noinspection DuplicatedCode
class Planet(pw.Model):
    id = pw.IntegerField()
    lang = pw.CharField(max_length=5)
    race = pw.CharField(max_length=10)
    name = pw.CharField(max_length=50)

    class Meta:
        table_name = "planet"
        primary_key = pw.CompositeKey('id', 'lang', 'race')
        indexes = [(('id', 'lang', 'race'), False),
                   (('lang', 'race'), False),
                   (('name',), False)]


# noinspection DuplicatedCode
class Star(pw.Model):
    id = pw.IntegerField()
    lang = pw.CharField(max_length=5)
    name = pw.CharField(max_length=50)
    size = pw.CharField(max_length=50, null=True)

    class Meta:
        table_name = "star"
        primary_key = pw.CompositeKey('id', 'lang')
        indexes = [(('id', 'lang'), False),
                   (('lang',), False),
                   (('name',), False)]


# noinspection PyUnusedLocal
def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    Star.insert_many(
        STARS,
        fields=[Star.id, Star.lang, Star.name, Star.size]
    ).execute(database=database)

    Planet.insert_many(
        PLANETS,
        fields=[Planet.id, Planet.lang, Planet.race, Planet.name]
    ).execute(database=database)


# noinspection PyUnusedLocal
def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.sql('DELETE FROM star WHERE TRUE;')
    migrator.sql('DELETE FROM planet WHERE TRUE;')
