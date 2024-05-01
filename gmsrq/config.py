import logging
from dataclasses import dataclass

log = logging.getLogger()


@dataclass
class Config:
    users_dir: str
    quests_dir: str
    #
    act_url: str
    img_url: str
    snd_url: str
    track_url: str
    #
    cgi_url: str
    reg_url: str
    reg_add_url: str
    reg_del_url: str
    opts_url: str
    opts_pass_url: str


def err_handler(func):
    def decorator(*agrs, **kwargs):
        try:
            return func(*agrs, **kwargs)
        except Exception as ex:
            log.warning(f'{ex}', exc_info=ex)
            return 50, f'{ex}'
    return decorator
