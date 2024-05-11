import logging
from os.path import dirname, realpath

import gmcapsule
from peewee_migrate import Router

import gmsrq
from gmsrq.migrations import MIGRATE_DIR
from gmsrq.sqlstore import db

CGI_URL = '/cgi/'
QUEST_DIR = f'{dirname(realpath(__file__))}/borrowed/qm'
USERS_DIR = f'{dirname(realpath(__file__))}/users'


def init(capsule: gmcapsule.Context):
    """Extension module initialization."""
    srq_cfg = gmsrq.Config(
        users_dir=USERS_DIR, quests_dir=QUEST_DIR,
        root_dir=capsule.cfg.root_dir(),
        act_url=f'{CGI_URL}act',
        img_url='/quests/img/',
        snd_url='/quests/snd/',
        track_url='/quests/track/',
        cgi_url=CGI_URL,
        reg_url=f'{CGI_URL}reg',
        reg_add_url=f'{CGI_URL}reg/add/',
        opts_url=f'{CGI_URL}opts',
        opts_pass_url=f'{CGI_URL}opts/pass',
        opts_del_acc_url=f'{CGI_URL}opts/del/acc/',
        opts_del_cert_url=f'{CGI_URL}opts/del/cert/',
        opts_rename_url=f'{CGI_URL}opts/rename/')

    db.database = USERS_DIR + '/gmsrq.sqlite'
    router = Router(db, migrate_dir=MIGRATE_DIR, logger=logging.getLogger())
    router.run()
    gmsrq.GmQuestsHandler(srq_cfg).init(capsule)
    gmsrq.GmUsersHandler(srq_cfg).init(capsule)


# Local GmCapsule for testing
# TODO: Make gmcapsule pytest-able
if __name__ == '__main__':
    gm_cfg = gmcapsule.Config('./config-local.ini')
    gmcapsule.Capsule(gm_cfg).run()
