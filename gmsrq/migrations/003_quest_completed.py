import peewee as pw
from peewee_migrate import Migrator


# noinspection PyUnusedLocal
def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    @migrator.create_model
    class QuestCompleted(pw.Model):
        ranger = pw.ForeignKeyField(column_name='rId', field='id',
                                    model=migrator.orm['ranger'],
                                    on_delete='cascade')
        quest = pw.ForeignKeyField(column_name='qId', field='id',
                                   model=migrator.orm['quest'])

        class Meta:
            table_name = "questcompleted"
            primary_key = pw.CompositeKey('ranger', 'quest')
            indexes = [(('ranger',), False), (('quest',), False)]


# noinspection PyUnusedLocal
def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.remove_model('questcompleted')
