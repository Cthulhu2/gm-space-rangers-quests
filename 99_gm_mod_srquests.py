import logging
from os.path import dirname, realpath

import gmcapsule
import gmsrq

log = logging.getLogger()

CGI_URL = '/cgi/'
CGI_ACT_URL = f'{CGI_URL}act'
CGI_REG_URL = f'{CGI_URL}reg'
CGI_REG_ADD_URL = f'{CGI_URL}reg/add/'
CGI_REG_DEL_URL = f'{CGI_URL}reg/del/'
CGI_OPTS_URL = f'{CGI_URL}opts'
CGI_OPTS_PASS_URL = f'{CGI_URL}opts/pass'
QUEST_DIR = f'{dirname(realpath(__file__))}/borrowed/qm'
USERS_DIR = f'{dirname(realpath(__file__))}/users'


def init(capsule: gmcapsule.Context):
    """Extension module initialization."""
    q_cfg = gmsrq.Config(users_dir=USERS_DIR, quests_dir=QUEST_DIR,
                         act_url=CGI_ACT_URL,
                         img_url='/quests/img/',
                         snd_url='/quests/snd/',
                         track_url='/quests/track/')

    gm_quests = gmsrq.GmQuestsHandler(q_cfg)
    capsule.add(CGI_ACT_URL, gm_quests.handle)
    #
    gm_users = gmsrq.GmUsersHandler(users_dir=USERS_DIR,
                                    reg_url=CGI_REG_URL,
                                    opts_url=CGI_OPTS_URL,
                                    reg_add_url=CGI_REG_ADD_URL,
                                    reg_del_url=CGI_REG_DEL_URL)
    capsule.add(CGI_URL, gm_users.handle)
    capsule.add(CGI_REG_ADD_URL + '*', gm_users.handle_reg_add)
    capsule.add(CGI_REG_DEL_URL + '*', gm_users.handle_reg_del)
    capsule.add(CGI_REG_URL + '*', gm_users.handle_reg)
    capsule.add(CGI_OPTS_URL, gm_users.handle_opts)
    capsule.add(CGI_OPTS_PASS_URL, gm_users.handle_opts_pass)


# Local GmCapsule for testing
# TODO: Make gmcapsule pytest-able
if __name__ == "__main__":
    cfg = gmcapsule.Config('./config-local.ini')
    gmcapsule.Capsule(cfg).run()
