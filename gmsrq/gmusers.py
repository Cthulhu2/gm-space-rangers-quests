import logging
import urllib.parse
from datetime import datetime
from typing import Callable
from urllib.parse import parse_qs

import gmcapsule

from gmsrq.page_index import meta, page_index
from gmsrq.sqlstore import IpOptions, Cert, db, Options, Ranger
from gmsrq.utils import Config, err_handler, mark_ranger_activity

log = logging.getLogger()


def parse_query(query: str):
    params = parse_qs(query)
    return str(params['lang'][0]) if 'lang' in params else None


def parse_opts_query(query: str):
    params = parse_qs(query)
    return (params['save'][0].lower() == 't' if 'save' in params else None,
            params['ansi'][0].lower() == 't' if 'ansi' in params else None)


def hello_ranger(_, ranger: Ranger, lang):
    return 20, meta(lang), (
            _('Wow! This is the famous ranger {name}!').format(name=ranger.name)
            + ' ' + _('You are already registered.') + '\n'
            + f'=> /{lang}/ 🔙 ' + _('Back') + '\n')


def ask_name(_):
    return 10, _('What is your name?')


def ask_name_to_attach(_):
    return 10, _('Enter ranger\'s name to attach certificate to.')


def ask_del_cert(_, cert: str):
    return 10, _('Delete certificate {cert}.'
                 ' Are you sure? Type "yes".').format(cert=cert[0:10].upper())


def ask_del_acc(_, ranger: Ranger):
    return 10, _('Delete ranger {name} account and all its data.'
                 ' Are you sure? Type "yes".').format(name=ranger.name)


def ask_password(_):
    return 11, _('Password?')


def is_valid_name(name: str):
    return (name and len(name) < 128
            and not any((x in name for x in ('```', '\r', '\n'))))


def invalid_name(_, lang: str):
    return 20, meta(lang), _(
        'Invalid ranger name. Not allowed:\n'
        '* >=128 symbols -- database is not rubber;\n'
        '* \\r, \\n -- what are these rangers with line breaks;\n'
        '* ``` -- and we don’t need to break the formatting.')


def options(_, cfg, ranger: Ranger, fp_cert):
    opts = ranger.get_opts()
    ansi = opts.ansi
    certs = ranger.get_certs()
    name = ranger.name or next(filter(lambda c: c.fp == fp_cert, certs)).subj
    certs_items = options_certs(_, cfg, ranger.name, certs, fp_cert,
                                opts.get_pass_expires())
    rename_ranger = (f'=> {cfg.opts_rename_url} ' + _('Rename ranger') + '\n\n'
                     if not ranger.is_anon else '')
    return (
            f'# ' + _('Options') + '\n' +
            f'=> {cfg.cgi_url} 🔙 ' + _('Back') + '\n\n' +
            f'=> {cfg.opts_url}?save=t&ansi={"f" if ansi else "t"}'
            f' {"☑" if ansi else "☐"} ' + _('Use ANSI-colors') + '\n\n' +
            f'{certs_items}\n'
            f'## ' + _('Account') + '\n' +
            f'{rename_ranger}'
            f'=> {cfg.opts_del_acc_url} ⚠ ' + _('Delete ranger {name}')
            .format(name=name) + '\n' +
            _('All quests progress and registered certificates'
              ' will be deleted') + '\n'
    )


def options_certs(_, cfg: Config, username, certs, fp_cert, pass_expires_ts):
    if not username:
        return ''  # no certificates management for unregistered users
    minutes = pass_expires_minutes(pass_expires_ts)
    expires = _('valid {minutes} min').format(minutes=minutes) if minutes \
        else _('not set')
    certs_items = (
            f'## ' + _('Certificates') + '\n' +
            f'=> {cfg.opts_pass_url} 🔑 ' + _('Certificate password ({expires})')
            .format(expires=expires) + '\n' +
            _('For adding other certificates you need set password.'
              ' Then just try register for this username.') + '\n\n' +
            f'### ' + _('Registered to {name}').format(name=username) + '\n'
    )
    for c in certs:
        title = cert_title(c)
        if fp_cert == c.fp:
            certs_items += (f'{title}\n' +
                            _('(current)') + '\n\n')
        else:
            certs_items += (
                    f'{title}\n' +
                    f'=> {cfg.opts_del_cert_url}{c} ✘ ' + _('Remove') + '\n\n')
    return certs_items


def cert_title(cert: Cert):
    expire = datetime.strftime(cert.expire, "%Y-%m-%d") if cert.expire else '-'
    return f'{cert.fp[0:10].upper()} · Expires {expire} · Subject: {cert.subj}'


def pass_expires_minutes(pass_expires_ts):
    if not pass_expires_ts:
        return None
    pass_expires_sec = (pass_expires_ts - datetime.utcnow()).total_seconds()
    return int(pass_expires_sec / 60) if pass_expires_sec > 0 else None


def already_used(_, reg_url: str, reg_url_add: str, player: str, lang):
    return 20, meta(lang), (
            _('Ranger {name} already registered.').format(name=player) + '\n'
            + f'=> {reg_url} ' + _('Choose different name') + '\n'
            + f'=> {reg_url_add}/{urllib.parse.quote(player)} '
            + _('Yes, it is me') + '\n')


class GmUsersHandler:
    cfg: Config

    def __init__(self, cfg: Config):
        self.cfg = cfg

    def init(self, capsule: gmcapsule.Context):
        for lang in self.cfg.l10n.keys():
            capsule.add(f'/{lang}/', self.index)
            capsule.add(f'/{lang}/leaders', self.handle_leaders)
        # registration
        capsule.add(self.cfg.cgi_url, self.handle_cgi)
        capsule.add(self.cfg.reg_add_url + '*', self.handle_reg_add)
        capsule.add(self.cfg.reg_url + '*', self.handle_reg)
        # options
        capsule.add(self.cfg.opts_url, self.handle_opts)
        capsule.add(self.cfg.opts_pass_url, self.handle_opts_pass)
        capsule.add(self.cfg.opts_del_cert_url + '*', self.handle_opts_del_cert)
        capsule.add(self.cfg.opts_del_acc_url + '*', self.handle_opts_del_acc)
        capsule.add(self.cfg.opts_rename_url + '*', self.handle_opts_rename)

    def gettext_(self, lang: str) -> Callable[[str], str]:
        return self.cfg.l10n[lang].gettext if lang in self.cfg.l10n \
            else self.cfg.l10n['en'].gettext

    def ask_cert(self, remote_addr):
        _ = self.gettext_(IpOptions.lang_by_ip(remote_addr))
        return 60, _('Ranger certificate required')

    @err_handler
    @mark_ranger_activity
    def index(self, req: gmcapsule.gemini.Request):
        lang = req.path.split('/')[1]
        _ = self.gettext_(lang)
        if not req.identity:
            IpOptions.save_lang(req.remote_address[0], lang)
            return page_index(_, None, lang, self.cfg,
                              self.cfg.root_dir.joinpath(req.hostname))

        with db.atomic():
            ranger = Ranger.by(fp_cert=req.identity.fp_cert)
            if not ranger:
                IpOptions.save_lang(req.remote_address[0], lang)
                return page_index(_, None, lang, self.cfg,
                                  self.cfg.root_dir.joinpath(req.hostname))
            # re-save selected lang by cert
            Options.save_lang(req.identity.fp_cert, lang)
        return page_index(_, ranger, lang, self.cfg,
                          self.cfg.root_dir.joinpath(req.hostname))

    @err_handler
    @mark_ranger_activity
    def handle_cgi(self, req: gmcapsule.gemini.Request):
        # handle base /cgi/ to ask cert once, with saving selected language
        lang = parse_query(req.query)
        if not lang and not req.identity:
            return self.ask_cert(req.remote_address[0])

        if lang and not req.identity:
            # save selected lang by IP
            with db.atomic():
                IpOptions.save_lang(req.remote_address[0], lang)
            return 30, self.cfg.cgi_url  # to ask cert for all /cgi/* urls

        with db.atomic():
            ranger = Ranger.by(fp_cert=req.identity.fp_cert)
            if not ranger:
                lang = IpOptions.lang_by_ip(req.remote_address[0])
                Ranger.create_anon(req.identity)
                ranger = Ranger.by(fp_cert=req.identity.fp_cert)
            if lang:
                # re-save selected lang by cert
                Options.save_lang(req.identity.fp_cert, lang)
            else:
                lang = Options.lang_by(fp_cert=req.identity.fp_cert)
        _ = self.gettext_(lang)
        return page_index(_, ranger, lang, self.cfg,
                          self.cfg.root_dir.joinpath(req.hostname))

    @err_handler
    @mark_ranger_activity
    def handle_reg(self, req: gmcapsule.gemini.Request):
        if not req.identity:
            return self.ask_cert(req.remote_address[0])

        ranger = Ranger.by(fp_cert=req.identity.fp_cert)
        if not ranger:
            return 30, self.cfg.cgi_url  #
        lang = ranger.get_opts().lang
        _ = self.gettext_(lang)
        username = urllib.parse.unquote_plus(req.query or '')
        if not ranger.is_anon:
            return hello_ranger(_, ranger, lang)
        elif not is_valid_name(username):
            return ask_name(_)
        with db.atomic():
            if Ranger.exists_name(username):
                return already_used(_, self.cfg.reg_url, self.cfg.reg_add_url,
                                    username, lang)
            ranger.name = username
            ranger.is_anon = False
            ranger.save()
        return 30, self.cfg.opts_url

    @err_handler
    @mark_ranger_activity
    def handle_reg_add(self, req: gmcapsule.gemini.Request):
        if not req.identity:
            return self.ask_cert(req.remote_address[0])

        if not req.path.endswith('/'):
            return 30, req.path + '/'

        lang = Options.lang_by(fp_cert=req.identity.fp_cert)
        _ = self.gettext_(lang)
        path = req.path[len(self.cfg.reg_add_url):].split('/')
        if len(path) < 1:
            return ask_name_to_attach(_)
        username = urllib.parse.unquote_plus(path[0])
        if not is_valid_name(username):
            return invalid_name(_, lang)
        if not req.query:
            return ask_password(_)
        if Options.is_valid_pass(username, req.query):
            with db.atomic():
                ranger: Ranger = Ranger.by(name=username)
                anon: Ranger = Ranger.by(fp_cert=req.identity.fp_cert)
                anon_cert: Cert = Cert.by(fp_cert=req.identity.fp_cert)
                anon_cert.ranger = ranger
                anon_cert.save()
                anon.delete_instance()
            return 30, self.cfg.opts_url
        else:
            return 20, meta(lang), _('Password incorrect')

    @err_handler
    @mark_ranger_activity
    def handle_opts(self, req: gmcapsule.gemini.Request):
        if not req.identity:
            return self.ask_cert(req.remote_address[0])

        save, ansi = parse_opts_query(req.query)
        ranger = Ranger.by(fp_cert=req.identity.fp_cert)
        if not ranger:
            return 30, f'/{IpOptions.lang_by_ip(req.remote_address[0])}/'
        opts = ranger.get_opts()
        if save:
            if ansi is not None:
                opts.ansi = ansi
                opts.save()
        fp_cert = req.identity.fp_cert
        ranger = Ranger.by(fp_cert=fp_cert)
        _ = self.gettext_(opts.lang)
        return 20, meta(opts.lang), options(_, self.cfg, ranger, fp_cert)

    @err_handler
    @mark_ranger_activity
    def handle_opts_pass(self, req: gmcapsule.gemini.Request):
        if not req.identity:
            return self.ask_cert(req.remote_address[0])

        fp_cert = req.identity.fp_cert
        if req.query is None:
            _ = self.gettext_(Options.lang_by(fp_cert=fp_cert))
            return ask_password(_)
        Options.save_pass(fp_cert, req.query)
        return 30, self.cfg.opts_url

    @err_handler
    @mark_ranger_activity
    def handle_opts_del_cert(self, req: gmcapsule.gemini.Request):
        if not req.identity:
            return self.ask_cert(req.remote_address[0])

        if not req.path.endswith('/'):
            return 30, req.path + '/'

        path = req.path[len(self.cfg.opts_del_cert_url):].split('/')
        del_cert = path[0]
        if not req.query:
            _ = self.gettext_(Options.lang_by(fp_cert=req.identity.fp_cert))
            return ask_del_cert(_, del_cert)
        if 'yes' == req.query:
            with db.atomic():
                ranger: Ranger = Ranger.by(fp_cert=req.identity.fp_cert)
                cert = next(filter(lambda c: c.fp == del_cert,
                                   ranger.get_certs()), None)
                if cert:
                    cert.delete_instance()
        return 30, self.cfg.opts_url

    @err_handler
    @mark_ranger_activity
    def handle_opts_del_acc(self, req: gmcapsule.gemini.Request):
        if not req.identity:
            return self.ask_cert(req.remote_address[0])

        if not req.path.endswith('/'):
            return 30, req.path + '/'

        ranger = Ranger.by(fp_cert=req.identity.fp_cert)
        if not ranger:
            return 30, f'/{IpOptions.lang_by_ip(addr=req.remote_address[0])}/'
        lang = Options.lang_by(fp_cert=req.identity.fp_cert)
        if not req.query:
            _ = self.gettext_(lang)
            return ask_del_acc(_, ranger)
        if 'yes' == req.query:
            with db.atomic():
                ranger.delete_instance()
        return 30, f'/{lang}/'

    @err_handler
    @mark_ranger_activity
    def handle_opts_rename(self, req: gmcapsule.gemini.Request):
        if not req.identity:
            return self.ask_cert(req.remote_address[0])

        if not req.path.endswith('/'):
            return 30, req.path + '/'

        ranger = Ranger.by(fp_cert=req.identity.fp_cert)
        if not ranger:
            return 30, f'/{IpOptions.lang_by_ip(addr=req.remote_address[0])}/'
        lang = Options.lang_by(fp_cert=req.identity.fp_cert)
        _ = self.gettext_(lang)
        if not req.query:
            return ask_name(_)
        username = urllib.parse.unquote_plus(req.query)
        if not is_valid_name(username):
            return invalid_name(_, lang)
        #
        with db.atomic():
            if Ranger.exists_name(username):
                return 20, meta(lang), _('Ranger {name} already registered.') \
                    .format(name=username)
            ranger.name = username
            ranger.save()
        return 30, self.cfg.opts_url

    @err_handler
    @mark_ranger_activity
    def handle_leaders(self, req: gmcapsule.gemini.Request):
        lang = req.path.split('/')[1]
        _ = self.gettext_(lang)

        rid = None
        if req.identity:
            ranger = Ranger.by(fp_cert=req.identity.fp_cert)
            rid = ranger.id if ranger else None

        th = _('  # : Ranger                    : Quests : Credits')
        tl = f'----:---------------------------:--------:---------'
        rows = []
        for pos, row in enumerate(Ranger.leaders(lang=lang), 1):
            if row[0] == rid and pos > 1:
                rows.append(tl)
            rows.append(f'{pos:>3} : {row[1]:<25} : {row[2]:^6} : {row[3]}')
            if row[0] == rid and pos < 10:
                rows.append(tl)

        page = (f'# ' + _('Leader board') + '\n' +
                f'=> /{lang}/ 🔙 ' + _('Back') + '\n\n' +
                _('Only registered rangers are displayed.') + '\n' +
                f'```' + _('Leader board') + '\n' +
                th + '\n' +
                tl + '\n' +
                '\n'.join(rows) + '\n' +
                f'```\n')

        return 20, meta(lang), page
