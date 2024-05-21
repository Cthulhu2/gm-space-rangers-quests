import peewee as pw
from peewee_migrate import Migrator


# noinspection PyUnusedLocal
def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    # noinspection DuplicatedCode
    @migrator.create_model
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
    @migrator.create_model
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

    migrator.add_fields(
        'queststate',
        fromStar=pw.TextField(null=True),
        fromPlanet=pw.TextField(null=True),
        toPlanet=pw.TextField(null=True),
        toStar=pw.TextField(null=True))


# noinspection PyUnusedLocal
def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.remove_model('star')
    migrator.remove_model('planet')
    migrator.remove_fields('queststate',
                           'fromStar', 'fromPlanet', 'toPlanet', 'toStar')
