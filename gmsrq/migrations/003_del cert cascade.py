import peewee as pw
from peewee_migrate import Migrator


# noinspection PyUnusedLocal
def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    # AAAA!!!
    # Sqlite doesn't have ALTER COLUMN,
    # so recreate table with ON DELETE cascade
    migrator.sql('ALTER TABLE cert RENAME TO cert_old;')

    @migrator.create_model
    class Cert(pw.Model):
        fp = pw.CharField(max_length=64, primary_key=True)
        ranger = pw.ForeignKeyField(column_name='rId', field='id',
                                    model=migrator.orm['ranger'],
                                    on_delete='cascade')
        subj = pw.CharField(max_length=256, null=True)
        expire = pw.DateTimeField(null=True)

        class Meta:
            table_name = "cert"
            indexes = [(('ranger',), False), (('fp',), False)]

    migrator.sql('INSERT INTO cert (fp, rId, subj, expire)'
                 ' SELECT fp, rId, subj, expire FROM cert_old;')
    migrator.sql('DROP TABLE cert_old;')


# noinspection PyUnusedLocal,DuplicatedCode
def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.sql('ALTER TABLE cert RENAME TO cert_old;')

    @migrator.create_model
    class Cert(pw.Model):
        fp = pw.CharField(max_length=64, primary_key=True)
        ranger = pw.ForeignKeyField(column_name='rId', field='id',
                                    model=migrator.orm['ranger'])
        subj = pw.CharField(max_length=256, null=True)
        expire = pw.DateTimeField(null=True)

        class Meta:
            table_name = "cert"
            indexes = [(('ranger',), False), (('fp',), False)]

    migrator.sql('INSERT INTO cert (fp, rId, subj, expire)'
                 ' SELECT fp, rId, subj, expire FROM cert_old;')
    migrator.sql('DROP TABLE cert_old;')
