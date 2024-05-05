import peewee as pw
from peewee_migrate import Migrator


# noinspection PyUnusedLocal
def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    @migrator.create_model
    class Ranger(pw.Model):
        id = pw.IntegerField(primary_key=True)
        name = pw.CharField(max_length=128, null=True, unique=True)
        is_anon = pw.BooleanField(default=True)
        created = pw.DateTimeField()
        activity = pw.DateTimeField()

        class Meta:
            table_name = "ranger"

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

    @migrator.create_model
    class IpOptions(pw.Model):
        addr = pw.TextField(primary_key=True)
        lang = pw.CharField(default='en', max_length=5)

        class Meta:
            table_name = "ipoptions"

    @migrator.create_model
    class Options(pw.Model):
        ranger = pw.ForeignKeyField(column_name='rId', field='id',
                                    model=migrator.orm['ranger'],
                                    on_delete='cascade', primary_key=True)
        ansi = pw.BooleanField(default=False)
        lang = pw.CharField(default='en', max_length=5)
        passHash = pw.BlobField(null=True)
        passSalt = pw.BlobField(null=True)
        passWhen = pw.DateTimeField(null=True)

        class Meta:
            table_name = "options"
            indexes = [(('ranger',), False)]

    @migrator.create_model
    class Quest(pw.Model):
        id = pw.IntegerField(primary_key=True)
        name = pw.CharField(max_length=128)
        file = pw.CharField(max_length=128)
        lang = pw.CharField(max_length=5)
        gameVer = pw.CharField(max_length=128)

        class Meta:
            table_name = "quest"

    @migrator.create_model
    class QuestState(pw.Model):
        ranger = pw.ForeignKeyField(column_name='rId', field='id',
                                    model=migrator.orm['ranger'],
                                    on_delete='cascade')
        quest = pw.ForeignKeyField(column_name='qId', field='id',
                                   model=migrator.orm['quest'])
        state = pw.TextField()
        sId = pw.IntegerField()

        class Meta:
            table_name = "queststate"
            primary_key = pw.CompositeKey('ranger', 'quest')


# noinspection PyUnusedLocal
def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.remove_model('queststate')
    migrator.remove_model('quest')
    migrator.remove_model('options')
    migrator.remove_model('ipoptions')
    migrator.remove_model('cert')
    migrator.remove_model('ranger')
