import logging
import urllib.parse
from datetime import datetime
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


def ask_cert(lang: str = None):
    return 60, ('Требуется сертификат рейнджера' if lang == 'ru' else
                'Ranger certificate required')


def ask_name(lang: str):
    return 10, ('What is your name?' if lang == 'en' else
                'Как вас называть?')


def ask_name_to_attach(lang: str):
    return 10, (
        'Enter ranger\'s name to attach certificate to'
        if lang == 'en' else
        'Введите имя рейнджера для добавления сертификата'
    )


def ask_del_cert(lang: str, cert: str):
    return 10, (
        f'Delete certificate {cert[0:10].upper()}. Are you sure? Type "yes"'
        if lang == 'en' else
        f'Удалить сертификат {cert[0:10].upper()}. Вы уверены? Введите "yes"'
    )


def ask_del_acc(lang: str, ranger: Ranger):
    return 10, (
        f'Delete ranger {ranger.name} account and all its data.'
        f' Are you sure? Type "yes"'
        if lang == 'en' else
        f'Удалить аккаунт рейнджера {ranger.name} и все его данные.'
        f' Вы уверены? Введите "yes"'
    )


def ask_password(lang: str):
    return 11, ('Password?' if lang == 'en' else
                'Пароль?')


def is_valid_name(name: str):
    return (name and len(name) < 128
            and '```' not in name
            and '\r' not in name
            and '\n' not in name)


def invalid_name(lang: str):
    rules = invalid_name_en() if lang == 'en' else invalid_name_ru()
    return 20, meta(lang), (
        f'Invalid ranger name. {rules}' if lang == 'en' else
        f'Неподходяще имя для рейнджера. {rules}')


def invalid_name_en():
    return ('Not allowed:\n'
            '* >=128 symbols -- database is not rubber;\n'
            '* \\r, \\n -- what are these rangers with line breaks;\n'
            '* ``` -- and we don’t need to break the formatting.')


def invalid_name_ru():
    return ('Нельзя использовать:\n'
            '* >=128 символов -- база данных не резиновая;\n'
            '* \\r, \\n -- это что за рейнджеры с переносами строк;\n'
            '* ``` -- и форматирование нам ломать не надо.')


def opts_en(cfg, ranger: Ranger, fp_cert):
    opts = ranger.get_opts()
    ansi = opts.ansi
    certs = ranger.get_certs()
    cert = next(filter(lambda c: c.fp == fp_cert, certs), None)
    certs_items = opts_en_certs(cfg, ranger.name, certs, fp_cert,
                                opts.get_pass_expires())
    ranger_name = ranger.name or cert.subj
    rename_ranger = (f'=> {cfg.opts_rename_url} Rename ranger\n\n'
                     if not ranger.is_anon else '')
    return (
        f'# Options\n'
        f'=> {cfg.cgi_url} Back\n\n'
        f'=> {cfg.opts_url}?save=t&ansi={"f" if ansi else "t"}'
        f' {"☑" if ansi else "☐"} Use ANSI-colors\n'
        f'\n'
        f'{certs_items}\n'
        f'## Account\n'
        f'{rename_ranger}'
        f'=> {cfg.opts_del_acc_url} ⚠ Delete ranger {ranger_name}\n'
        f'All quests progress and registered certificates will be deleted\n'
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
            certs_items += f'{title}\n' \
                           f'(current)\n\n'
        else:
            certs_items += f'{title}\n' \
                           f'=> {cfg.opts_del_cert_url}{c} ✘ Remove\n\n'
    return certs_items


def cert_title(cert: Cert):
    expire = datetime.strftime(cert.expire, "%Y-%m-%d") if cert.expire else '-'
    return f'{cert.fp[0:10].upper()} · Expires {expire} · Subject: {cert.subj}'


def opts_ru(cfg, ranger: Ranger, fp_cert):
    opts = ranger.get_opts()
    ansi = opts.ansi
    certs = ranger.get_certs()
    cert = next(filter(lambda c: c.fp == fp_cert, certs), None)
    certs_items = opts_ru_certs(cfg, ranger.name, certs, fp_cert,
                                opts.get_pass_expires())
    ranger_name = ranger.name or cert.subj
    rename_ranger = (f'=> {cfg.opts_rename_url} Переименовать рейнджера\n\n'
                     if not ranger.is_anon else '')
    return (
        f'# Опции\n'
        f'=> {cfg.cgi_url} Назад\n\n'
        f'=> {cfg.opts_url}?save=t&ansi={"f" if ansi else "t"}'
        f' {"☑" if ansi else "☐"} Использовать ANSI-цвета\n'
        f'\n'
        f'{certs_items}\n'
        f'## Аккаунт\n'
        f'{rename_ranger}'
        f'=> {cfg.opts_del_acc_url} ⚠ Удалить рейнджера {ranger_name}\n'
        f'Будет удалён весь прогресс и все связанные сертификаты\n'
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
            certs_items += f'{title}\n' \
                           f'(текущий)\n\n'
        else:
            certs_items += f'{title}\n' \
                           f'=> {cfg.opts_del_cert_url}{c} ✘ Удалить\n\n'
    return certs_items


def pass_expires_minutes(pass_expires_ts):
    if not pass_expires_ts:
        return None
    pass_expires_sec = (pass_expires_ts - datetime.utcnow()).total_seconds()
    return int(pass_expires_sec / 60) if pass_expires_sec > 0 else None


def already_used(reg_url: str, reg_url_add_ident: str, player: str, lang):
    return 20, meta(lang), (
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
        capsule.add(self.cfg.cgi_url, self.handle_cgi)
        capsule.add(self.cfg.reg_add_url + '*', self.handle_reg_add)
        capsule.add(self.cfg.reg_url + '*', self.handle_reg)
        # options
        capsule.add(self.cfg.opts_url, self.handle_opts)
        capsule.add(self.cfg.opts_pass_url, self.handle_opts_pass)
        capsule.add(self.cfg.opts_del_cert_url + '*', self.handle_opts_del_cert)
        capsule.add(self.cfg.opts_del_acc_url + '*', self.handle_opts_del_acc)
        capsule.add(self.cfg.opts_rename_url + '*', self.handle_opts_rename)

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
                IpOptions.save_lang(req.remote_address[0], lang)
                return page_index(None, lang, self.cfg,
                                  self.cfg.root_dir.joinpath(req.hostname))
            # re-save selected lang by cert
            Options.save_lang(req.identity.fp_cert, lang)
        return page_index(ranger, lang, self.cfg,
                          self.cfg.root_dir.joinpath(req.hostname))

    @err_handler
    @mark_ranger_activity
    def handle_cgi(self, req: gmcapsule.gemini.Request):
        # handle base /cgi/ to ask cert once, with saving selected language
        lang = parse_query(req.query)
        if not lang and not req.identity:
            return ask_cert(IpOptions.lang_by_ip(req.remote_address[0]))

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

        return page_index(ranger, lang, self.cfg,
                          self.cfg.root_dir.joinpath(req.hostname))

    @err_handler
    @mark_ranger_activity
    def handle_reg(self, req: gmcapsule.gemini.Request):
        if not req.identity:
            return ask_cert(IpOptions.lang_by_ip(req.remote_address[0]))

        ranger = Ranger.by(fp_cert=req.identity.fp_cert)
        if not ranger:
            return 30, self.cfg.cgi_url  #
        lang = ranger.get_opts().lang
        username = urllib.parse.unquote_plus(req.query or '')
        if not ranger.is_anon:
            return 20, meta(lang), hello_ranger(ranger, lang)
        elif not is_valid_name(username):
            return ask_name(lang)
        with db.atomic():
            if Ranger.exists_name(username):
                return already_used(self.cfg.reg_url, self.cfg.reg_add_url,
                                    username, lang)
            ranger.name = username
            ranger.is_anon = False
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
        username = urllib.parse.unquote_plus(path[0])
        if not is_valid_name(username):
            return invalid_name(lang)
        if not req.query:
            return ask_password(lang)
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
            return 20, meta(lang), ('Password incorrect' if lang == 'en' else
                                    'Неправильный пароль')

    @err_handler
    @mark_ranger_activity
    def handle_opts(self, req: gmcapsule.gemini.Request):
        if not req.identity:
            return ask_cert(IpOptions.lang_by_ip(req.remote_address[0]))

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
        if opts.lang == 'en':
            return 20, meta(opts.lang), opts_en(self.cfg, ranger, fp_cert)
        else:
            return 20, meta(opts.lang), opts_ru(self.cfg, ranger, fp_cert)

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

    @err_handler
    @mark_ranger_activity
    def handle_opts_del_cert(self, req: gmcapsule.gemini.Request):
        if not req.identity:
            return ask_cert(IpOptions.lang_by_ip(req.remote_address[0]))

        if not req.path.endswith('/'):
            return 30, req.path + '/'

        path = req.path[len(self.cfg.opts_del_cert_url):].split('/')
        del_cert = path[0]
        if not req.query:
            lang = Options.lang_by(fp_cert=req.identity.fp_cert)
            return ask_del_cert(lang, del_cert)
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
            return ask_cert(IpOptions.lang_by_ip(req.remote_address[0]))

        if not req.path.endswith('/'):
            return 30, req.path + '/'

        ranger = Ranger.by(fp_cert=req.identity.fp_cert)
        if not ranger:
            return 30, f'/{IpOptions.lang_by_ip(addr=req.remote_address[0])}/'
        lang = Options.lang_by(fp_cert=req.identity.fp_cert)
        if not req.query:
            return ask_del_acc(lang, ranger)
        if 'yes' == req.query:
            with db.atomic():
                ranger.delete_instance()
        return 30, f'/{lang}/'

    @err_handler
    @mark_ranger_activity
    def handle_opts_rename(self, req: gmcapsule.gemini.Request):
        if not req.identity:
            return ask_cert(IpOptions.lang_by_ip(req.remote_address[0]))

        if not req.path.endswith('/'):
            return 30, req.path + '/'

        ranger = Ranger.by(fp_cert=req.identity.fp_cert)
        if not ranger:
            return 30, f'/{IpOptions.lang_by_ip(addr=req.remote_address[0])}/'
        lang = Options.lang_by(fp_cert=req.identity.fp_cert)
        if not req.query:
            return ask_name(lang)
        username = urllib.parse.unquote_plus(req.query)
        if not is_valid_name(username):
            return invalid_name(lang)
        with db.atomic():
            if Ranger.exists_name(username):
                return 20, meta(lang), (
                    f'Ranger {username} already registered.'
                    if lang == 'en' else
                    f'Рейнджер {username} уже зарегистрирован.'
                )
            ranger.name = username
            ranger.save()
        return 30, self.cfg.opts_url
