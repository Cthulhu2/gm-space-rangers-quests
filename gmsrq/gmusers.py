import logging
from datetime import datetime
from os.path import join, islink, isdir
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


def hello_ranger(ranger: Ranger, lang):
    if lang == 'en':
        return f'Wow! This is the famous ranger, {ranger.name}!' \
               f' You are already registered.\n' \
               f'=> /{lang}/ Back\n'
    else:
        return f'Ба! Да это же знаменитый рейнджер, {ranger.name}!' \
               f' Вы уже зарегистрированы.\n' \
               f'=> /{lang}/ Назад\n'


def is_already_registered(cert_dir):
    return islink(cert_dir)


def is_username_used(users_dir, username):
    user_dir = join(users_dir, username)
    return isdir(user_dir)


def is_valid_name(name: str):
    return name and len(name) < 128


def ask_cert(lang: str = None):
    return 60, (
        'Требуется сертификат рейнджера'
        if lang == 'ru' else
        'Ranger certificate required'
    )


def ask_name(lang: str):
    return 10, 'What is your name?' if lang == 'en' else 'Как вас называть?'


def ask_name_to_attach(lang: str):
    return 10, (
        'Enter username to attach certificate'
        if lang == 'en' else
        'Введите имя пользователя для добавления сертификата'
    )


def ask_del_cert(lang: str, cert: str):
    return 10, (
        f'Del certificate {cert[0:10].upper()}. Are you sure? Type "yes"'
        if lang == 'en' else
        f'Удалить сертификат {cert[0:10].upper()}. Точно? Введите "yes"'
    )


def ask_password(lang: str):
    return 10, 'Password?' if lang == 'en' \
        else 'Пароль?'


def opts_en(cfg, ranger: Ranger, fp_cert):
    opts = ranger.get_opts()
    ansi = opts.ansi
    certs_items = opts_en_certs(cfg, ranger.name, ranger.get_certs(), fp_cert,
                                opts.get_pass_expires())
    return (
        f'# Options\n'
        f'=> {cfg.opts_url}?save=t&ansi={"f" if ansi else "t"}'
        f' {"☑" if ansi else "☐"} Use ANSI-colors\n'
        f'\n'
        f'{certs_items}\n'
        f'=> /en/ Back\n'
    )


def opts_en_certs(cfg: Config, username, certs, fp_cert, pass_expires_ts):
    if not username:
        return ''  # no certificates management for unregistered users
    minutes = pass_expires_minutes(pass_expires_ts)
    expires = f'valid {minutes} min' if minutes else 'not set'
    certs_items = (
        f'## Certificates\n'
        f'=> {cfg.opts_pass_url} 🔑 Certificate password ({expires})\n'
        'For adding other certificates you need set password.'
        ' Then just try register for this username.\n\n'
        f'### Registered to {username}\n'
    )
    for c in certs:
        title = cert_title(c)
        if fp_cert == c.fp:
            certs_items += f'{title} (current)\n\n'
        else:
            certs_items += f'{title}\n' \
                           f'=> {cfg.reg_del_url}{c} ✘ Remove\n\n'
    return certs_items


def cert_title(cert: Cert):
    expire = datetime.strftime(cert.expire, "%Y-%m-%d") if cert.expire else '-'
    return f'{cert.fp[0:10].upper()} · Expires {expire} · Subject: {cert.subj}'


def opts_ru(cfg, ranger: Ranger, fp_cert):
    opts = ranger.get_opts()
    ansi = opts.ansi
    certs_items = opts_ru_certs(cfg, ranger.name, ranger.get_certs(), fp_cert,
                                opts.get_pass_expires())
    return (
        f'# Опции\n'
        f'=> {cfg.opts_url}?save=t&ansi={"f" if ansi else "t"}'
        f' {"☑" if ansi else "☐"} Использовать ANSI-цвета\n'
        f'\n'
        f'{certs_items}\n'
        f'=> /ru/ Назад\n'
    )


def opts_ru_certs(cfg: Config, username, certs, fp_cert, pass_expires_ts):
    if not username:
        return ''  # no certificates management for unregistered users
    minutes = pass_expires_minutes(pass_expires_ts)
    expires = f'на {minutes} мин' if minutes else 'не установлен'
    certs_items = (
        f'## Сертификаты\n'
        f'=> {cfg.opts_pass_url} 🔑 Пароль на сертификаты ({expires})\n'
        f'Для добавления других сертификатов нужно установить пароль.'
        f' Потом просто просто попытаться зарегистрировать на этот логин.\n\n'
        f'### Зарегистрировано на {username}\n'
    )
    for c in certs:
        title = cert_title(c)
        if fp_cert == c.fp:
            certs_items += f'{title} (текущий)\n\n'
        else:
            certs_items += f'{title}\n' \
                           f'=> {cfg.reg_del_url}{c} ✘ Удалить\n\n'
    return certs_items


def pass_expires_minutes(pass_expires_ts):
    if not pass_expires_ts:
        return None
    pass_expires_sec = (pass_expires_ts - datetime.utcnow()).total_seconds()
    return int(pass_expires_sec / 60) if pass_expires_sec > 0 else None


def already_used(reg_url: str, reg_url_add_ident: str, player: str, lang):
    return (
        (f'Ranger {player} already registered.\n'
         f'=> {reg_url} Choose different name\n'
         f'=> {reg_url_add_ident}/{player} Yes, it is me\n')
        if lang == 'en' else
        (f'Рейнджер {player} уже зарегистрирован.\n'
         f'=> {reg_url} Выберу другое имя\n'
         f'=> {reg_url_add_ident}/{player} Да, это я\n')
    )


class GmUsersHandler:
    cfg: Config

    def __init__(self, cfg: Config):
        self.cfg = cfg

    def init(self, capsule: gmcapsule.Context):
        # index
        capsule.add('/en/', self.index)
        capsule.add('/ru/', self.index)
        # registration
        capsule.add(self.cfg.cgi_url, self.handle)
        capsule.add(self.cfg.reg_add_url + '*', self.handle_reg_add)
        capsule.add(self.cfg.reg_del_url + '*', self.handle_reg_del)
        capsule.add(self.cfg.reg_url + '*', self.handle_reg)
        # options
        capsule.add(self.cfg.opts_url, self.handle_opts)
        capsule.add(self.cfg.opts_pass_url, self.handle_opts_pass)

    @err_handler
    @mark_ranger_activity
    def index(self, req: gmcapsule.gemini.Request):
        lang = req.path.split('/')[1]
        if not req.identity:
            IpOptions.save_lang(req.remote_address[0], lang)
            return page_index(None, lang, self.cfg,
                              self.cfg.root_dir.joinpath(req.hostname))

        with db.atomic():
            ranger = Ranger.by(fp_cert=req.identity.fp_cert)
            if not ranger:
                Ranger.create_anon(req.identity)
                ranger = Ranger.by(fp_cert=req.identity.fp_cert)
            # re-save selected lang by cert
            Options.save_lang(req.identity.fp_cert, lang)
            return page_index(ranger, lang, self.cfg,
                              self.cfg.root_dir.joinpath(req.hostname))

    @err_handler
    @mark_ranger_activity
    def handle(self, req: gmcapsule.gemini.Request):
        # handle base /cgi/ to ask cert once, with saving selected language
        lang = parse_query(req.query)
        if not lang and not req.identity:
            return ask_cert(IpOptions.lang_by_ip(req.remote_address[0]))

        if lang and not req.identity:
            # save selected lang by IP
            with db.atomic():
                IpOptions.save_lang(req.remote_address[0], lang)
            return 30, self.cfg.cgi_url  # to ask cert for all /cgi/* urls
        if not lang and req.identity:
            lang = IpOptions.lang_by_ip(req.remote_address[0])

        with db.atomic():
            Ranger.create_anon(req.identity)
            # re-save selected lang by cert
            Options.save_lang(req.identity.fp_cert, lang)
        return 30, self.cfg.reg_url

    @err_handler
    @mark_ranger_activity
    def handle_reg(self, req: gmcapsule.gemini.Request):
        if not req.identity:
            return ask_cert(IpOptions.lang_by_ip(req.remote_address[0]))

        ranger = Ranger.by(fp_cert=req.identity.fp_cert)
        lang = ranger.get_opts().lang
        if not ranger.is_anon:
            return 20, meta(lang), hello_ranger(ranger, lang)
        elif not is_valid_name(req.query):
            return ask_name(lang)
        with db.atomic():
            if Ranger.exists_name(req.query):
                return (20, meta(lang),
                        already_used(self.cfg.reg_url, self.cfg.reg_add_url,
                                     req.query, lang))
            ranger.name = req.query
            ranger.is_anon = False
            ranger.activity = datetime.now()
            ranger.save()
        return 30, self.cfg.opts_url

    @err_handler
    @mark_ranger_activity
    def handle_reg_add(self, req: gmcapsule.gemini.Request):
        if not req.identity:
            return ask_cert(IpOptions.lang_by_ip(req.remote_address[0]))

        if not req.path.endswith('/'):
            return 30, req.path + '/'

        lang = Options.lang_by(fp_cert=req.identity.fp_cert)
        path = req.path[len(self.cfg.reg_add_url):].split('/')
        if len(path) < 1:
            return ask_name_to_attach(lang)
        username = path[0]
        if not is_valid_name(username):
            return 50, f'Invalid username'
        if not req.query:
            return ask_password(lang)
        if Options.is_valid_pass(username, req.query):
            with db.atomic():
                ranger: Ranger = Ranger.by(name=username)
                anon: Ranger = Ranger.by(fp_cert=req.identity.fp_cert)
                anon_cert: Cert = Cert.by(fp_cert=req.identity.fp_cert)
                anon_cert.ranger = ranger
                anon_cert.save()
                ranger.activity = datetime.now()
                ranger.save()
                anon.delete_instance()

        return 30, self.cfg.opts_url

    @err_handler
    @mark_ranger_activity
    def handle_reg_del(self, req: gmcapsule.gemini.Request):
        if not req.identity:
            return ask_cert(IpOptions.lang_by_ip(req.remote_address[0]))

        if not req.path.endswith('/'):
            return 30, req.path + '/'

        path = req.path[len(self.cfg.reg_del_url):].split('/')
        del_cert = path[0]
        if not req.query:
            lang = Options.lang_by(fp_cert=req.identity.fp_cert)
            return ask_del_cert(lang, del_cert)
        if 'yes' == req.query:
            with db.atomic():
                ranger: Ranger = Ranger.by(fp_cert=req.identity.fp_cert)
                ranger.activity = datetime.now()
                ranger.save()
                cert = Cert.by(fp_cert=del_cert)
                if cert in ranger.get_certs():
                    cert.delete_instance()
        return 30, self.cfg.opts_url

    @err_handler
    @mark_ranger_activity
    def handle_opts(self, req: gmcapsule.gemini.Request):
        lang = parse_query(req.query)
        if not req.identity:
            return ask_cert(lang)

        if not lang:
            lang = Options.lang_by(fp_cert=req.identity.fp_cert)
        else:
            Options.save_lang(req.identity.fp_cert, lang)
        return self.opts(req, lang)

    def opts(self, req: gmcapsule.gemini.Request, lang):
        save, ansi = parse_opts_query(req.query)
        ranger = Ranger.by(fp_cert=req.identity.fp_cert)
        if not ranger:
            with db.atomic():
                Ranger.create_anon(req.identity)
                ranger = Ranger.by(fp_cert=req.identity.fp_cert)
        opts = ranger.get_opts()
        if save:
            if ansi is not None:
                opts.ansi = ansi
                opts.save()
        fp_cert = req.identity.fp_cert
        ranger = Ranger.by(fp_cert=fp_cert)
        if lang == 'en':
            return 20, meta(lang), opts_en(self.cfg, ranger, fp_cert)
        else:
            return 20, meta(lang), opts_ru(self.cfg, ranger, fp_cert)

    @err_handler
    @mark_ranger_activity
    def handle_opts_pass(self, req: gmcapsule.gemini.Request):
        if not req.identity:
            return ask_cert(IpOptions.lang_by_ip(req.remote_address[0]))

        fp_cert = req.identity.fp_cert
        if req.query is None:
            return ask_password(Options.lang_by(fp_cert=fp_cert))
        Options.save_pass(fp_cert, req.query)
        return 30, self.cfg.opts_url
