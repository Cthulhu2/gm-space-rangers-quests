import logging
import os
import re
from datetime import datetime
from os import listdir
from os.path import join, islink, isdir
from pathlib import Path
from shutil import rmtree, move
from urllib.parse import parse_qs

import gmcapsule

from gmsrq.store import save_lang, load_lang, load_ansi, save_ansi, \
    get_username, get_user_certs, is_valid_pass, del_user_cert, set_pass, \
    save_cert_info, get_cert_info, get_pass_expires

log = logging.getLogger()

VALID_NAME_REGEX = r'^[a-zA-Zа-яА-ЯёЁ\d\-_\.]*$'


def parse_query(query: str):
    params = parse_qs(query)
    return str(params['lang'][0]) if 'lang' in params else None


def parse_opts_query(query: str):
    params = parse_qs(query)
    return (params['save'][0].lower() == 't' if 'save' in params else None,
            params['ansi'][0].lower() == 't' if 'ansi' in params else None)


def hello_ranger(cert_dir: str, lang: str):
    player = Path(cert_dir).readlink().name
    if lang == 'en':
        return f'Wow! This is the famous ranger, {player}!' \
               f' You are already registered.\n' \
               f'=> /{lang}/ Back\n'
    else:
        return f'Ба! Да это же знаменитый рейнджер, {player}!' \
               f' Вы уже зарегистрированы.\n' \
               f'=> /{lang}/ Назад\n'


def is_already_registered(cert_dir):
    return islink(cert_dir)


def is_username_used(users_dir, username):
    user_dir = join(users_dir, username)
    return isdir(user_dir)


def is_valid_name(name: str):
    return name and len(name) < 125 and re.match(VALID_NAME_REGEX, name)


def ask_cert(lang: str = None):
    return 60, (
        'Ranger certificate required'
        if lang == 'en' else
        'Требуется сертификат рейнджера'
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
        f'Del certificate {cert[0:10]}. Are you sure? Type "yes"'
        if lang == 'en' else
        f'Удалить сертификат {cert[0:10]}. Точно? Введите "yes"'
    )


def ask_password(lang: str):
    return 10, 'Password?' if lang == 'en' \
        else 'Пароль?'


def opts_en(url, ansi, username, fp_cert, certs=None, pass_expires_ts=None):
    certs_items = opts_en_certs(username, certs, fp_cert, pass_expires_ts)
    return (
        f'# Options\n'
        f'=> {url}?save=t&ansi={"f" if ansi else "t"} {"☑" if ansi else "☐"}'
        f' Use ANSI-colors\n'
        f'\n'
        f'{certs_items}\n'
        f'=> /en/ Back\n'
    )


def opts_en_certs(username, certs, fp_cert, pass_expires_ts):
    if not username:
        return ''  # no certificates management for unregistered users
    minutes = pass_expires_minutes(pass_expires_ts)
    expires = f'valid {minutes} min' if minutes else 'not set'
    certs_items = (
        f'## Certificates\n'
        f'=> /cgi/opts/pass 🔑 Certificate password ({expires})\n'
        'For adding other certificates you need set password.'
        ' Then just try register for this username.\n\n'
        f'### Registered to {username}\n'
    )
    for c, info in certs:
        title = cert_title(c, info)
        if fp_cert == c:
            certs_items += f'{title} (current)\n\n'
        else:
            certs_items += f'{title}\n' \
                           f'=> /cgi/reg/del/{c} ✘ Remove\n\n'
    return certs_items


def cert_title(cert: str, info):
    return (f'{cert[0:10].upper()}'
            f' · Expires {datetime.strftime(info[1], "%Y-%m-%d")}'
            f' · Subject: {info[0]}'
            if info else cert[0:10].upper())


def opts_ru(url, ansi, username, fp_cert, certs=None, pass_expires_ts=None):
    certs_items = opts_ru_certs(username, certs, fp_cert, pass_expires_ts)
    return (
        f'# Опции\n'
        f'=> {url}?save=t&ansi={"f" if ansi else "t"} {"☑" if ansi else "☐"}'
        f' Использовать ANSI-цвета\n'
        f'\n'
        f'{certs_items}\n'
        f'=> /ru/ Назад\n'
    )


def opts_ru_certs(username, certs, fp_cert, pass_expires_ts):
    if not username:
        return ''  # no certificates management for unregistered users
    minutes = pass_expires_minutes(pass_expires_ts)
    expires = f'на {minutes} мин' if minutes else 'не установлен'
    certs_items = (
        f'## Сертификаты\n'
        f'=> /cgi/opts/pass 🔑 Пароль на сертификаты ({expires})\n'
        f'Для добавления других сертификатов нужно установить пароль.'
        f' Потом просто просто попытаться зарегистрировать на этот логин.\n\n'
        f'### Зарегистрировано на {username}\n'
    )
    for c, info in certs:
        title = cert_title(c, info)
        if fp_cert == c:
            certs_items += f'{title} (текущий)\n\n'
        else:
            certs_items += f'{title}\n' \
                           f'=> /cgi/reg/del/{c} ✘ Удалить\n\n'
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
    users_dir: str
    reg_url: str
    reg_add_url: str
    reg_del_url: str
    opts_url: str

    def __init__(self, users_dir: str, reg_url: str,
                 reg_add_url: str, reg_del_url: str, opts_url):
        self.users_dir = users_dir
        self.reg_url = reg_url
        self.reg_add_url = reg_add_url
        self.reg_del_url = reg_del_url
        self.opts_url = opts_url

    def handle(self, req: gmcapsule.gemini.Request):
        # handle base /cgi/ to ask cert once, with saving selected language
        lang = parse_query(req.query)
        if not lang and not req.identity:
            lang = load_lang(self.users_dir, req.remote_address[0])
            return ask_cert(lang)
        try:
            if lang and not req.identity:
                # save selected lang by IP
                save_lang(self.users_dir, req.remote_address[0], lang)
                return 30, '/cgi/'  # to ask cert for all /cgi/* urls
            if not lang and req.identity:
                # re-save selected lang by cert
                lang = load_lang(self.users_dir, req.remote_address[0])
                save_lang(self.users_dir, req.identity.fp_cert, lang)
            return 30, self.reg_url
        except Exception as ex:
            log.warning(f'{ex}', exc_info=ex)
            return 50, f'{ex}'

    def handle_reg(self, req: gmcapsule.gemini.Request):
        lang = load_lang(self.users_dir, req.remote_address[0])
        if not req.identity:
            return ask_cert(lang)
        try:
            lang = lang or load_lang(self.users_dir, req.identity.fp_cert)
            cert_dir = join(self.users_dir, req.identity.fp_cert)
            if is_already_registered(cert_dir):
                save_lang(self.users_dir, req.identity.fp_cert, lang)
                return hello_ranger(cert_dir, lang)
            elif not is_valid_name(req.query):
                return ask_name(lang)
            elif is_username_used(self.users_dir, req.query):
                return already_used(self.reg_url, self.reg_add_url,
                                    req.query, lang)
            return self.register(req)
        except Exception as ex:
            log.warning(f'{ex}', exc_info=ex)
            return 50, f'{ex}'

    def handle_reg_add(self, req: gmcapsule.gemini.Request):
        if not req.identity:
            lang = load_lang(self.users_dir, req.remote_address[0])
            return ask_cert(lang)
        try:
            lang = load_lang(self.users_dir, req.identity.fp_cert)
            if not req.path.endswith('/'):
                return 30, req.path + '/'
            path = req.path[len(self.reg_add_url):].split('/')
            if len(path) < 1:
                return ask_name_to_attach(lang)
            username = path[0]
            if not is_valid_name(username):
                return 50, f'Invalid username'
            if not req.query:
                return ask_password(lang)
            if is_valid_pass(self.users_dir, username, req.query):
                self.attach(username, req.identity)
            return 30, self.opts_url
        except Exception as ex:
            log.warning(f'{ex}', exc_info=ex)
            return 50, f'{ex}'

    def handle_reg_del(self, req: gmcapsule.gemini.Request):
        if not req.identity:
            lang = load_lang(self.users_dir, req.remote_address[0])
            return ask_cert(lang)
        try:
            lang = load_lang(self.users_dir, req.identity.fp_cert)
            if not req.path.endswith('/'):
                return 30, req.path + '/'
            path = req.path[len(self.reg_del_url):].split('/')
            del_cert = path[0]
            if not req.query:
                return ask_del_cert(lang, del_cert)
            if 'yes' == req.query:
                username = get_username(self.users_dir, req.identity.fp_cert)
                if del_cert in get_user_certs(self.users_dir, username):
                    del_user_cert(self.users_dir, del_cert)
            return 30, self.opts_url
        except Exception as ex:
            log.warning(f'{ex}', exc_info=ex)
            return 50, f'{ex}'

    def attach(self, username, ident: gmcapsule.Identity):
        cert_dir = join(self.users_dir, ident.fp_cert)
        user_dir = join(self.users_dir, username)
        rmtree(cert_dir, ignore_errors=True)

        try:
            Path(cert_dir).symlink_to(user_dir, True)
        except FileExistsError:
            pass
        save_cert_info(self.users_dir, ident)

    def register(self, req: gmcapsule.gemini.Request):
        user_dir = join(self.users_dir, req.query)
        cert_dir = join(self.users_dir, req.identity.fp_cert)
        lang = load_lang(self.users_dir, req.identity.fp_cert)

        os.makedirs(user_dir, exist_ok=True)
        if isdir(cert_dir):
            for file in listdir(cert_dir):
                move(join(cert_dir, file), user_dir)
            rmtree(cert_dir, ignore_errors=True)
        Path(cert_dir).symlink_to(user_dir, True)
        save_cert_info(self.users_dir, req.identity)
        return 30, f'/{lang}/'

    def handle_opts(self, req: gmcapsule.gemini.Request):
        lang = parse_query(req.query)
        if not req.identity:
            return ask_cert(lang)
        try:
            if not lang:
                lang = load_lang(self.users_dir, req.identity.fp_cert)
            else:
                save_lang(self.users_dir, req.identity.fp_cert, lang)
            return self.opts(req, lang)
        except Exception as ex:
            log.warning(f'{ex}', exc_info=ex)
            return 50, f'{ex}'

    def opts(self, req: gmcapsule.gemini.Request, lang):
        save, ansi = parse_opts_query(req.query)
        fp_cert = req.identity.fp_cert
        if save:
            if ansi is not None:
                save_ansi(self.users_dir, fp_cert, ansi)
        ansi = load_ansi(self.users_dir, fp_cert)
        username = get_username(self.users_dir, fp_cert)
        user_certs = get_user_certs(self.users_dir, username)
        if user_certs:
            user_certs = [(c, get_cert_info(self.users_dir, c))
                          for c in user_certs]
        pass_expires_ts = get_pass_expires(self.users_dir, username)
        if lang == 'en':
            return opts_en(self.opts_url, ansi, username, fp_cert, user_certs,
                           pass_expires_ts)
        else:
            return opts_ru(self.opts_url, ansi, username, fp_cert, user_certs,
                           pass_expires_ts)

    def handle_opts_pass(self, req: gmcapsule.gemini.Request):
        if not req.identity:
            return ask_cert()
        try:
            fp_cert = req.identity.fp_cert
            lang = load_lang(self.users_dir, fp_cert)
            if req.query is None:
                return ask_password(lang)
            set_pass(self.users_dir, fp_cert, req.query)
            return 30, self.opts_url
        except Exception as ex:
            log.warning(f'{ex}', exc_info=ex)
            return 50, f'{ex}'
