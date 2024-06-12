import peewee as pw
from peewee_migrate import Migrator


# noinspection PyUnusedLocal
def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    # migrator.add_fields recreate ranger's related tables???
    # queststate, questcompleted, options
    migrator.sql('ALTER TABLE ranger ADD COLUMN credits_en'
                 '  INTEGER NOT NULL DEFAULT 2000;')
    migrator.sql('ALTER TABLE ranger ADD COLUMN credits_ru'
                 '  INTEGER NOT NULL DEFAULT 2000;')


# noinspection PyUnusedLocal
def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.sql('ALTER TABLE ranger DROP COLUMN credits_ru;')
    migrator.sql('ALTER TABLE ranger DROP COLUMN credits_en;')
