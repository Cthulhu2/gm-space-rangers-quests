import peewee as pw
from peewee_migrate import Migrator


# noinspection PyUnusedLocal
def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    # migrator.add_fields recreate ranger's related tables???
    # cert, queststate, questcompleted, options
    migrator.sql('ALTER TABLE ranger ADD COLUMN credits_cze'
                 '  INTEGER NOT NULL DEFAULT 2000;')
    migrator.sql('ALTER TABLE ranger ADD COLUMN credits_fr'
                 '  INTEGER NOT NULL DEFAULT 2000;')
    migrator.sql('ALTER TABLE ranger ADD COLUMN credits_hu'
                 '  INTEGER NOT NULL DEFAULT 2000;')
    migrator.sql('ALTER TABLE ranger ADD COLUMN credits_pl'
                 '  INTEGER NOT NULL DEFAULT 2000;')


# noinspection PyUnusedLocal
def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.sql('ALTER TABLE ranger DROP COLUMN credits_cze;')
    migrator.sql('ALTER TABLE ranger DROP COLUMN credits_fr;')
    migrator.sql('ALTER TABLE ranger DROP COLUMN credits_hu;')
    migrator.sql('ALTER TABLE ranger DROP COLUMN credits_pl;')
