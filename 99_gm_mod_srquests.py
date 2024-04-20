import logging
from os.path import dirname, realpath

import gmcapsule
import gmsrq

log = logging.getLogger()

CGI_URL = '/cgi/'
QUEST_DIR = f'{dirname(realpath(__file__))}/borrowed/qm'
USERS_DIR = f'{dirname(realpath(__file__))}/users'


def init(capsule: gmcapsule.Context):
    """Extension module initialization."""
    srq_cfg = gmsrq.Config(
        users_dir=USERS_DIR, quests_dir=QUEST_DIR,
        act_url=f'{CGI_URL}act',
        img_url='/quests/img/',
        snd_url='/quests/snd/',
        track_url='/quests/track/',
        cgi_url=CGI_URL,
        reg_url=f'{CGI_URL}reg',
        reg_add_url=f'{CGI_URL}reg/add/',
        reg_del_url=f'{CGI_URL}reg/del/',
        opts_url=f'{CGI_URL}opts',
        opts_pass_url=f'{CGI_URL}opts/pass')

    gmsrq.GmQuestsHandler(srq_cfg).init(capsule)
    gmsrq.GmUsersHandler(srq_cfg).init(capsule)


# Local GmCapsule for testing
# TODO: Make gmcapsule pytest-able
if __name__ == '__main__':
    gm_cfg = gmcapsule.Config('./config-local.ini')
    gmcapsule.Capsule(gm_cfg).run()
