import peewee as pw
from peewee_migrate import Migrator


# noinspection PyUnusedLocal
def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.add_fields('ranger', credits_en=pw.IntegerField(default=2000))
    migrator.add_fields('ranger', credits_ru=pw.IntegerField(default=2000))


# noinspection PyUnusedLocal
def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.remove_fields('ranger', 'credits_en')
    migrator.remove_fields('ranger', 'credits_ru')
