from os.path import dirname, realpath

from .utils import Config
from .gmquests import GmQuestsHandler
from .gmusers import GmUsersHandler

MIGRATE_DIR = f'{dirname(realpath(__file__))}/migrations'
