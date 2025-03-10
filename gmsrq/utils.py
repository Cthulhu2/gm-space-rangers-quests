import logging
from dataclasses import dataclass
from gettext import GNUTranslations
from pathlib import Path
from typing import Dict

from gmcapsule.gemini import Request

from gmsrq.sqlstore import Ranger

log = logging.getLogger()


@dataclass
class Config:
    l10n: Dict[str, GNUTranslations]
    users_dir: str
    quests_dir: str
    root_dir: Path
    #
    act_url: str
    img_url: str
    snd_url: str
    track_url: str
    #
    cgi_url: str
    sort_url: str
    reg_url: str
    reg_add_url: str
    opts_url: str
    opts_pass_url: str
    opts_del_acc_url: str
    opts_del_cert_url: str
    opts_rename_url: str


def err_handler(func):
    def decorator(*agrs, **kwargs):
        try:
            return func(*agrs, **kwargs)
        except Exception as ex:
            log.warning(f'{ex}', exc_info=ex)
            return 50, f'{ex}'

    return decorator


def mark_ranger_activity(func):
    def decorator(*args, **kwargs):
        req: Request = next(filter(lambda arg: isinstance(arg, Request), args),
                            None)
        if req and req.identity:
            Ranger.update_activity(req.identity.fp_cert)
        return func(*args, **kwargs)

    return decorator


def meta(lang):
    return f'text/gemini; charset=utf-8; lang={lang}'


def site_title(_):
    return _('Ranger Center "Union"')
