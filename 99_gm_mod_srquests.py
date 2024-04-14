import logging
from os.path import dirname, realpath

import gmcapsule
import gmsrq

log = logging.getLogger()

ACTION_URL = '/cgi-quests/action'
QUEST_DIR = f'{dirname(realpath(__file__))}/borrowed/qm'
USERS_DIR = f'{dirname(realpath(__file__))}/users'


def init(capsule: gmcapsule.Context):
    """Extension module initialization."""
    q_cfg = gmsrq.Config(users_dir=USERS_DIR, quests_dir=QUEST_DIR,
                         action_url=ACTION_URL,
                         img_url='/quests/img/',
                         snd_url='/quests/snd/',
                         track_url='/quests/track/')

    gm_quests = gmsrq.GmQuestsHandler(q_cfg)

    capsule.add(ACTION_URL, gm_quests.handle)


# Local GmCapsule for testing
# TODO: Make gmcapsule pytest-able
if __name__ == "__main__":
    cfg = gmcapsule.Config('./config-local.ini')
    gmcapsule.Capsule(cfg).run()
