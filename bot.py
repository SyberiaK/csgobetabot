import time
import pandas as pd
import telebot
from telebot import types
import logging
import random
import validators


import config
from addons import strings, buttons, tags, datacenters, file_manager, util
from apps import xhair_sharecode, profiles


bot = telebot.AsyncTeleBot(config.BOT_TOKEN, parse_mode='html')
telebot.logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s | %(message)s', datefmt='%H:%M:%S — %d/%m/%Y')
CIS_lang_codes = ['ru', 'uk', 'be', 'uz', 'kk']


### Server statistics ###


def server_stats(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.from_user.language_code in CIS_lang_codes:
        text = '📊 Воспользуйтесь одной из приведённых команд:'
        markup = buttons.markup_ss_ru
    else:
        text = '📊 Use one of the following commands:'
        markup = buttons.markup_ss_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, server_stats_process)


def server_stats_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    log(message)
    if message.text.lower() in ('service status', 'состояние служб'):
        send_server_status(message)
    elif message.text.lower() in ('matchmaking status', 'состояние матчмейкинга'):
        send_mm_stats(message)
    elif message.text.lower() in ('dataсenters status', 'состояние дата-центров'):
        dc(message)
    elif message.text in ('⏪ Back', '⏪ Назад'):
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_ru
        else:
            markup = buttons.markup_en
        back(message, markup)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_ss_ru
        else:
            markup = buttons.markup_ss_en
        unknown_request(message, markup, server_stats_process)


def send_server_status(message):
    '''Send the status of CS:GO servers'''
    try:
        status_text_en, status_text_ru = util.server_status()
        if message.from_user.language_code in CIS_lang_codes:
            text = status_text_ru
            markup = buttons.markup_ss_ru
        else:
            text = status_text_en
            markup = buttons.markup_ss_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        msg = msg.wait()
        bot.register_next_step_handler(msg, server_stats_process)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)


def send_mm_stats(message):
    '''Send CS:GO matchamaking statistics'''
    try:
        mm_stats_text_en, mm_stats_text_ru = util.mm_stats()
        if message.from_user.language_code in CIS_lang_codes:
            text = mm_stats_text_ru
            markup = buttons.markup_ss_ru
        else:
            text = mm_stats_text_en
            markup = buttons.markup_ss_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        msg = msg.wait()
        bot.register_next_step_handler(msg, server_stats_process)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)


### Extra features ###


def extra_features(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.from_user.language_code in CIS_lang_codes:
        text = '🗃 Воспользуйтесь одной из приведённых команд:'
        markup = buttons.markup_extra_ru
    else:
        text = '🗃 Use one of the following commands:'
        markup = buttons.markup_extra_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, extra_features_process)


def extra_features_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    log(message)
    if message.text.lower() in ('🆕 crosshair', '🆕 прицел'):
        crosshair(message)
    elif message.text.lower() in ('developers in-game', 'разработчиков в игре'):
        send_devcount(message)
    elif message.text.lower() in ('game version', 'версия игры'):
        send_gameversion(message)
    elif message.text.lower() in ('cap reset', 'сброс ограничений'):
        send_timer(message)
    elif message.text.lower() in ('gun database', 'база данных оружий'):
        guns(message)
    elif message.text in ('⏪ Back', '⏪ Назад'):
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_ru
        else:
            markup = buttons.markup_en
        back(message, markup)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_extra_ru
        else:
            markup = buttons.markup_extra_en
        unknown_request(message, markup, extra_features_process)


def crosshair(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '🔖 Выберите желаемую функцию:'
        markup = buttons.markup_crosshair_ru
    else:
        text = '🔖 Select the desired function:'
        markup = buttons.markup_crosshair_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, crosshair_process)


def crosshair_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    log(message)
    if message.text.lower() in ('generate', 'создать'):
        encode(message)
    elif message.text.lower() in ('decode', 'расшифровать'):
        decode(message)
    elif message.text in ('⏪ Back', '⏪ Назад'):
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_extra_ru
        else:
            markup = buttons.markup_extra_en
        back(message, markup, extra_features_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_crosshair_ru
        else:
            markup = buttons.markup_crosshair_en
        unknown_request(message, markup, crosshair_process)


def encode(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '💤 В разработке..'
        markup = buttons.crosshair_ru
    else:
        text = '💤 Work in progress..'
        markup = buttons.crosshair_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, crosshair_process)


def decode(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = strings.xhair_decode_ru
        markup = buttons.markup_del
    else:
        text = strings.xhair_decode_en
        markup = buttons.markup_del
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, decode_proccess)


def decode_proccess(message):
    bot.send_chat_action(message.chat.id, 'typing')
    log(message)
    if message.text == '/cancel':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_crosshair_ru
        else:
            markup = buttons.markup_crosshair_en
        cancel(message, markup, crosshair_process)
    else:
        try:
            data = xhair_sharecode.decode(message.text)
            if not data:
                if message.from_user.language_code in CIS_lang_codes:
                    text = '⚠️ Неверный код, пожалуйста, попробуйте ещё раз.\n\nИспользуйте /cancel, чтобы отменить команду.'
                else:
                    text = '⚠️ Invalid code, please, try again.\n\nUse /cancel to cancel this command.'
                msg = bot.send_message(message.chat.id, text)
                msg = msg.wait()
                bot.register_next_step_handler(msg, decode_proccess)
                
            else:
                parameters = ''
                for x, y in data.items():
                    parameters += x + ' '
                    parameters += str(y) + '; '
                if message.from_user.language_code in CIS_lang_codes:
                    text = '🧬 Расшифрованные параметры данного кода прицела:\n\n' + f'<code>{parameters}</code>'
                    markup = buttons.markup_crosshair_ru
                else:
                    text = '🧬 Decoded parameters for the given crosshair code:\n\n' + f'<code>{parameters}</code>'
                    markup = buttons.markup_crosshair_en
                msg = bot.send_message(message.chat.id, text, reply_markup=markup)
                msg = msg.wait()
                bot.register_next_step_handler(msg, crosshair_process)
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)


def send_devcount(message):
    '''Send the count of online devs'''
    try:
        devcount_text_en, devcount_text_ru = util.devcount()
        if message.from_user.language_code in CIS_lang_codes:
            text = devcount_text_ru
            markup = buttons.markup_extra_ru
        else:
            text = devcount_text_en
            markup = buttons.markup_extra_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        msg = msg.wait()
        bot.register_next_step_handler(msg, extra_features_process)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)


def send_timer(message):
    '''Send drop cap reset time'''
    try:
        timer_text_en, timer_text_ru = util.timer()
        if message.from_user.language_code in CIS_lang_codes:
            text = timer_text_ru
            markup = buttons.markup_extra_ru
        else:
            text = timer_text_en
            markup = buttons.markup_extra_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        msg = msg.wait()
        bot.register_next_step_handler(msg, extra_features_process)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)


def send_gameversion(message):
    '''Send the version of the game'''
    try:
        gameversion_text_en, gameversion_text_ru = util.gameversion()
        if message.from_user.language_code in CIS_lang_codes:
            text = gameversion_text_ru
            markup = buttons.markup_extra_ru
        else:
            text = gameversion_text_en
            markup = buttons.markup_extra_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        msg = msg.wait()
        bot.register_next_step_handler(msg, extra_features_process)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)


def guns(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '#️⃣ Выберите категорию, которая Вас интересует:'
        markup = buttons.markup_guns_ru
    else:
        text = '#️⃣ Select the category, that you are interested in:'
        markup = buttons.markup_guns_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, guns_process)


def guns_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    log(message)
    if message.text.lower() in ('pistols', 'пистолеты'):
        pistols(message)
    elif message.text.lower() in ('smgs', 'пистолеты-пулемёты'):
        smgs(message)
    elif message.text.lower() in ('rifles', 'винтовки'):
        rifles(message)
    elif message.text.lower() in ('heavy', 'тяжёлое оружие'):
        heavy(message)
    elif message.text in ('⏪ Back', '⏪ Назад'):
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_extra_ru
        else:
            markup = buttons.markup_extra_en
        back(message, markup, extra_features_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_guns_ru
        else:
            markup = buttons.markup_guns_en
        unknown_request(message, markup, guns_process)


def pistols(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '🔫 Выберите пистолет:'
        markup = buttons.markup_pistols_ru
    else:
        text = '🔫 Select the pistol:'
        markup = buttons.markup_pistols_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, pistols_process)


def pistols_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    log(message)
    if message.text.lower() in tags.gun_name_list:
        for gName, gId in zip(tags.gun_name_list, tags.gun_id_list):
            if message.text.lower() == gName:
                send_gun_info(message, gId)
    elif message.text in ('⏪ Back', '⏪ Назад'):
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_guns_ru
        else:
            markup = buttons.markup_guns_en
        back(message, markup, guns_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_pistols_ru
        else:
            markup = buttons.markup_pistols_en
        unknown_request(message, markup, pistols_process)


def smgs(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '🔫 Выберите пистолет-пулемёт:'
        markup = buttons.markup_smgs_ru
    else:
        text = '🔫 Select the SMG:'
        markup = buttons.markup_smgs_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, smgs_process)


def smgs_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    log(message)
    if message.text.lower() in tags.gun_name_list:
        for gName, gId in zip(tags.gun_name_list, tags.gun_id_list):
            if message.text.lower() == gName:
                send_gun_info(message, gId)
    elif message.text in ('⏪ Back', '⏪ Назад'):
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_guns_ru
        else:
            markup = buttons.markup_guns_en
        back(message, markup, guns_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_smgs_ru
        else:
            markup = buttons.markup_smgs_en
        unknown_request(message, markup, smgs_process)


def rifles(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '🔫 Выберите винтовку:'
        markup = buttons.markup_rifles_ru
    else:
        text = '🔫 Select the rifle:'
        markup = buttons.markup_rifles_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, rifles_process)


def rifles_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    log(message)
    if message.text.lower() in tags.gun_name_list:
        for gName, gId in zip(tags.gun_name_list, tags.gun_id_list):
            if message.text.lower() == gName:
                send_gun_info(message, gId)
    elif message.text in ('⏪ Back', '⏪ Назад'):
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_guns_ru
        else:
            markup = buttons.markup_guns_en
        back(message, markup, guns_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_rifles_ru
        else:
            markup = buttons.markup_rifles_en
        unknown_request(message, markup, rifles_process)


def heavy(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '🔫 Выберите тяжёлое оружие:'
        markup = buttons.markup_heavy_ru
    else:
        text = '🔫 Select the heavy gun:'
        markup = buttons.markup_heavy_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, heavy_process)


def heavy_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    log(message)
    if message.text.lower() in tags.gun_name_list:
        for gName, gId in zip(tags.gun_name_list, tags.gun_id_list):
            if message.text.lower() == gName:
                send_gun_info(message, gId)
    elif message.text in ('⏪ Back', '⏪ Назад'):
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_guns_ru
        else:
            markup = buttons.markup_guns_en
        back(message, markup, guns_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_heavy_ru
        else:
            markup = buttons.markup_heavy_en
        unknown_request(message, markup, heavy_process)


def send_gun_info(message, gun_id):
    '''Send archived data about guns'''
    try:
        gun_data_text_en, gun_data_text_ru = util.gun_info(gun_id)
        if message.from_user.language_code in CIS_lang_codes:
            text = gun_data_text_ru
            markup = buttons.markup_guns_ru
        else:
            text = gun_data_text_en
            markup = buttons.markup_guns_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        msg = msg.wait()
        bot.register_next_step_handler(msg, guns_process)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)


### Profile information ###


def profile_info(message):
    bot.send_chat_action(message.chat.id, 'typing')
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        if message.from_user.language_code in CIS_lang_codes:
            text = '📖 Воспользуйтесь одной из приведённых команд:'
            markup = buttons.markup_profile_ru
        else:
            text = '📖 Use one of the following commands:'
            markup = buttons.markup_profile_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        msg = msg.wait()
        bot.register_next_step_handler(msg, profile_info_process)
    else:
        send_about_maintenance(message)


def profile_info_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    log(message)
    if message.text.lower() in ('bans and restrictions', 'запреты и ограничения'):
        temptag = 'bans'
        url(message, temptag)
    elif message.text.lower() in ('cs:go in-game statistics', 'игровая статистика cs:go'):
        temptag = 'stats'
        url(message, temptag)
    elif message.text in ('⏪ Back', '⏪ Назад'):
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_ru
        else:
            markup = buttons.markup_en
        back(message, markup)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_profile_ru
        else:
            markup = buttons.markup_profile_en
        unknown_request(message, markup, profile_info_process)


def url(message, temptag):
    if message.from_user.language_code in CIS_lang_codes:
        text = strings.url_ex_ru
        markup = buttons.markup_del
    else:
        text = strings.url_ex_en
        markup = buttons.markup_del
    msg = bot.send_message(message.chat.id, text,
                           reply_markup=markup, disable_web_page_preview=True)
    msg = msg.wait()
    bot.register_next_step_handler(msg, url_process, temptag)


def url_process(message, temptag):
    bot.send_chat_action(message.chat.id, 'typing')
    log(message)
    if temptag == 'bans':
        send_bans(message)
    else:
        send_stats(message)


def send_bans(message):
    if message.text == '/cancel':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_profile_ru
        else:
            markup = buttons.markup_profile_en
        cancel(message, markup, profile_info_process)
    else:
        try:
            bans_text_en, bans_text_ru = profiles.ban_info(message.text)
            if message.from_user.language_code in CIS_lang_codes:
                text = bans_text_ru
                markup = buttons.markup_profile_ru
            else:
                text = bans_text_en
                markup = buttons.markup_profile_en
            msg = bot.send_message(
                message.chat.id, text, reply_markup=markup, disable_web_page_preview=True)
            msg = msg.wait()
            bot.register_next_step_handler(msg, profile_info_process)
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)


def send_stats(message):
    if message.text == '/cancel':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_profile_ru
        else:
            markup = buttons.markup_profile_en
        cancel(message, markup, profile_info_process)
    else:
        try:
            url_en, url_ru = profiles.csgo_stats(message.text)
            if message.from_user.language_code in CIS_lang_codes:
                text = url_ru
                markup_share = types.InlineKeyboardMarkup()
                btn = types.InlineKeyboardButton(
                    'Поделиться', switch_inline_query=f'{text}')
                markup_share.add(btn)
            else:
                text = url_en
                markup_share = types.InlineKeyboardMarkup()
                btn = types.InlineKeyboardButton(
                    'Share', switch_inline_query=f'{text}')
                markup_share.add(btn)
            if message.from_user.language_code in CIS_lang_codes:
                text_followup = '📖 Воспользуйтесь одной из приведённых команд:'
                markup = buttons.markup_profile_ru
            else:
                text_followup = '📖 Use one of the following commands:'
                markup = buttons.markup_profile_en
            if validators.url(url_en):
                msg = bot.send_message(
                    message.chat.id, text, reply_markup=markup_share)
                msg = msg.wait()
                bot.send_message(
                    message.chat.id, text_followup, reply_markup=markup)
            else:
                msg = bot.send_message(
                    message.chat.id, text, reply_markup=markup)
                msg = msg.wait()
            bot.register_next_step_handler(msg, profile_info_process)
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)


### Datacenters ###


def dc(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '📶 Выберите регион, который Вам интересен, чтобы получить информацию о дата-центрах:'
        markup = buttons.markup_DC_ru
    else:
        text = '📶 Select the region, that you are interested in, to get information about the datacenters:'
        markup = buttons.markup_DC_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, dc_process)


def dc_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    log(message)
    if message.text.lower() in ('asia', 'азия'):
        dc_asia(message)
    elif message.text.lower() in ('south africa', 'южная африка'):
        send_dc_africa(message)
    elif message.text.lower() in ('australia', 'австралия'):
        send_dc_australia(message)
    elif message.text.lower() in ('europe', 'европа'):
        dc_europe(message)
    elif message.text.lower() in ('usa', 'сша'):
        dc_usa(message)
    elif message.text.lower() in ('south america', 'южная америка'):
        send_dc_south_america(message)
    elif message.text in ('⏪ Back', '⏪ Назад'):
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_ss_ru
        else:
            markup = buttons.markup_ss_en
        back(message, markup, server_stats_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_DC_ru
        else:
            markup = buttons.markup_DC_en
        unknown_request(message, markup, dc_process)


def dc_europe(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '📍 Укажите регион:'
        markup = buttons.markup_DC_EU_ru
    else:
        text = '📍 Specify the region:'
        markup = buttons.markup_DC_EU_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, dc_europe_process)


def dc_europe_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    log(message)
    if message.text.lower() in ('north', 'север'):
        send_dc_eu_north(message)
    elif message.text.lower() in ('east', 'восток'):
        send_dc_eu_east(message)
    elif message.text.lower() in ('west', 'запад'):
        send_dc_eu_west(message)
    elif message.text in ('⏪ Back', '⏪ Назад'):
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_DC_ru
        else:
            markup = buttons.markup_DC_en
        back(message, markup, dc_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_DC_EU_ru
        else:
            markup = buttons.markup_DC_EU_en
        unknown_request(message, markup, dc_europe_process)


def dc_usa(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '📍 Укажите регион:'
        markup = buttons.markup_DC_USA_ru
    else:
        text = '📍 Specify the region:'
        markup = buttons.markup_DC_USA_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, dc_usa_process)


def dc_usa_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    log(message)
    if message.text.lower() in ('north', 'север'):
        send_dc_usa_north(message)
    elif message.text.lower() in ('south', 'юг'):
        send_dc_usa_south(message)
    elif message.text in ('⏪ Back', '⏪ Назад'):
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_DC_ru
        else:
            markup = buttons.markup_DC_en
        back(message, markup, dc_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_DC_USA_ru
        else:
            markup = buttons.markup_DC_USA_en
        unknown_request(message, markup, dc_usa_process)


def dc_asia(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '📍 Укажите страну:'
        markup = buttons.markup_DC_Asia_ru
    else:
        text = '📍 Specify the country:'
        markup = buttons.markup_DC_Asia_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, dc_asia_process)


def dc_asia_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    log(message)
    if message.text.lower() in ('india', 'индия'):
        send_dc_india(message)
    elif message.text.lower() in ('japan', 'япония'):
        send_dc_japan(message)
    elif message.text.lower() in ('china', 'китай'):
        send_dc_china(message)
    elif message.text.lower() in ('emirates', 'эмираты'):
        send_dc_emirates(message)
    elif message.text.lower() in ('singapore', 'сингапур'):
        send_dc_singapore(message)
    elif message.text.lower() in ('hong kong', 'гонконг'):
        send_dc_hong_kong(message)
    elif message.text.lower() in ('south korea', 'южная корея'):
        send_dc_south_korea(message)
    elif message.text in ('⏪ Back', '⏪ Назад'):
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_DC_ru
        else:
            markup = buttons.markup_DC_en
        back(message, markup, dc_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_DC_Asia_ru
        else:
            markup = buttons.markup_DC_Asia_en
        unknown_request(message, markup, dc_asia_process)


def send_dc_africa(message):
    africa_text_en, africa_text_ru = datacenters.africa()
    if message.from_user.language_code in CIS_lang_codes:
        text = africa_text_ru
        markup = buttons.markup_DC_ru
    else:
        text = africa_text_en
        markup = buttons.markup_DC_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, dc_process)


def send_dc_australia(message):
    australia_text_en, australia_text_ru = datacenters.australia()
    if message.from_user.language_code in CIS_lang_codes:
        text = australia_text_ru
        markup = buttons.markup_DC_ru
    else:
        text = australia_text_en
        markup = buttons.markup_DC_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, dc_process)


def send_dc_eu_north(message):
    eu_north_text_en, eu_north_text_ru = datacenters.eu_north()
    if message.from_user.language_code in CIS_lang_codes:
        text = eu_north_text_ru
        markup = buttons.markup_DC_EU_ru
    else:
        text = eu_north_text_en
        markup = buttons.markup_DC_EU_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, dc_europe_process)


def send_dc_eu_west(message):
    eu_west_text_en, eu_west_text_ru = datacenters.eu_west()
    if message.from_user.language_code in CIS_lang_codes:
        text = eu_west_text_ru
        markup = buttons.markup_DC_EU_ru
    else:
        text = eu_west_text_en
        markup = buttons.markup_DC_EU_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, dc_europe_process)


def send_dc_eu_east(message):
    eu_east_text_en, eu_east_text_ru = datacenters.eu_east()
    if message.from_user.language_code in CIS_lang_codes:
        text = eu_east_text_ru
        markup = buttons.markup_DC_EU_ru
    else:
        text = eu_east_text_en
        markup = buttons.markup_DC_EU_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, dc_europe_process)


def send_dc_usa_north(message):
    usa_north_text_en, usa_north_text_ru = datacenters.usa_north()
    if message.from_user.language_code in CIS_lang_codes:
        text = usa_north_text_ru
        markup = buttons.markup_DC_USA_ru
    else:
        text = usa_north_text_en
        markup = buttons.markup_DC_USA_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, dc_usa_process)


def send_dc_usa_south(message):
    usa_south_text_en, usa_south_text_ru = datacenters.usa_south()
    if message.from_user.language_code in CIS_lang_codes:
        text = usa_south_text_ru
        markup = buttons.markup_DC_USA_ru
    else:
        text = usa_south_text_en
        markup = buttons.markup_DC_USA_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, dc_usa_process)


def send_dc_south_america(message):
    south_america_text_en, south_america_text_ru = datacenters.south_america()
    if message.from_user.language_code in CIS_lang_codes:
        text = south_america_text_ru
        markup = buttons.markup_DC_ru
    else:
        text = south_america_text_en
        markup = buttons.markup_DC_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, dc_process)


def send_dc_india(message):
    india_text_en, india_text_ru = datacenters.india()
    if message.from_user.language_code in CIS_lang_codes:
        text = india_text_ru
        markup = buttons.markup_DC_Asia_ru
    else:
        text = india_text_en
        markup = buttons.markup_DC_Asia_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, dc_asia_process)


def send_dc_japan(message):
    japan_text_en, japan_text_ru = datacenters.japan()
    if message.from_user.language_code in CIS_lang_codes:
        text = japan_text_ru
        markup = buttons.markup_DC_Asia_ru
    else:
        text = japan_text_en
        markup = buttons.markup_DC_Asia_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, dc_asia_process)


def send_dc_china(message):
    china_text_en, china_text_ru = datacenters.china()
    if message.from_user.language_code in CIS_lang_codes:
        text = china_text_ru
        markup = buttons.markup_DC_Asia_ru
    else:
        text = china_text_en
        markup = buttons.markup_DC_Asia_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, dc_asia_process)


def send_dc_emirates(message):
    emirates_text_en, emirates_text_ru = datacenters.emirates()
    if message.from_user.language_code in CIS_lang_codes:
        text = emirates_text_ru
        markup = buttons.markup_DC_Asia_ru
    else:
        text = emirates_text_en
        markup = buttons.markup_DC_Asia_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, dc_asia_process)


def send_dc_singapore(message):
    singapore_text_en, singapore_text_ru = datacenters.singapore()
    if message.from_user.language_code in CIS_lang_codes:
        text = singapore_text_ru
        markup = buttons.markup_DC_Asia_ru
    else:
        text = singapore_text_en
        markup = buttons.markup_DC_Asia_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, dc_asia_process)


def send_dc_hong_kong(message):
    hong_kong_text_en, hong_kong_text_ru = datacenters.hong_kong()
    if message.from_user.language_code in CIS_lang_codes:
        text = hong_kong_text_ru
        markup = buttons.markup_DC_Asia_ru
    else:
        text = hong_kong_text_en
        markup = buttons.markup_DC_Asia_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, dc_asia_process)


def send_dc_south_korea(message):
    south_korea_text_en, south_korea_text_ru = datacenters.south_korea()
    if message.from_user.language_code in CIS_lang_codes:
        text = south_korea_text_ru
        markup = buttons.markup_DC_Asia_ru
    else:
        text = south_korea_text_en
        markup = buttons.markup_DC_Asia_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    msg = msg.wait()
    bot.register_next_step_handler(msg, dc_asia_process)


def send_about_problem_bot(message):
    '''If anything goes wrong'''
    if message.from_user.language_code in CIS_lang_codes:
        text = strings.wrongBOT_ru
        markup = buttons.markup_ru
    else:
        text = strings.wrongBOT_en
        markup = buttons.markup_en
    bot.send_message(message.chat.id, text, reply_markup=markup)


def unknown_request(message, *args):
    if message.from_user.language_code in CIS_lang_codes:
        text = strings.unknownRequest_ru
        markup = buttons.markup_ru
    else:
        text = strings.unknownRequest_en
        markup = buttons.markup_en
    if len(args) < 1:
        bot.send_message(message.chat.id, text, reply_markup=markup)
    else:
        msg = bot.send_message(message.chat.id, text, reply_markup=args[0])
        msg = msg.wait()
        bot.register_next_step_handler(msg, args[1])


def back(message, *args):
    if len(args) < 2:
        bot.send_message(message.chat.id, '👌', reply_markup=args[0])
    else:
        msg = bot.send_message(message.chat.id, '👌', reply_markup=args[0])
        msg = msg.wait()
        bot.register_next_step_handler(msg, args[1])


def cancel(message, *args):
    if len(args) < 2:
        bot.send_message(message.chat.id, '👍', reply_markup=args[0])
    else:
        msg = bot.send_message(message.chat.id, '👍', reply_markup=args[0])
        msg = msg.wait()
        bot.register_next_step_handler(msg, args[1])


def pmOnly(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = 'Эта команда работает только в личных сообщениях.'
    else:
        text = 'This command only works in private messages.'
    msg = bot.send_message(message.chat.id, text,
                           reply_to_message_id=message.message_id)
    msg = msg.wait()
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    time.sleep(10)
    bot.delete_message(msg.chat.id, msg.message_id)


### Commands ###


@bot.message_handler(commands=['start'])
def welcome(message):
    '''First bot's message'''
    if message.chat.type == 'private':
        bot.send_chat_action(message.chat.id, 'typing')
        log(message)
        data = pd.read_csv(config.USER_DB_FILE_PATH)
        if not data['UserID'].isin([message.from_user.id]).any():
            new_data = pd.DataFrame([[message.from_user.first_name, message.from_user.id,
                                    message.from_user.language_code]], columns=['Name', 'UserID', 'Language'])
            pd.concat([data, new_data]).to_csv(
                config.USER_DB_FILE_PATH, index=False)
        if message.from_user.language_code in CIS_lang_codes:
            text = strings.cmdStart_ru.format(message.from_user.first_name)
            markup = buttons.markup_ru
        else:
            text = strings.cmdStart_en.format(message.from_user.first_name)
            markup = buttons.markup_en
        bot.send_message(message.chat.id, text, reply_markup=markup)
    else:
        pmOnly(message)


@bot.message_handler(commands=['feedback'])
def leave_feedback(message):
    '''Send feedback'''
    if message.chat.type == 'private':
        bot.send_chat_action(message.chat.id, 'typing')
        log(message)
        if message.from_user.language_code in CIS_lang_codes:
            text = strings.cmdFeedback_ru
        else:
            text = strings.cmdFeedback_en
        msg = bot.send_message(message.chat.id, text,
                               reply_markup=buttons.markup_del)
        msg = msg.wait()
        bot.register_next_step_handler(msg, get_feedback)
    else:
        pmOnly(message)


def get_feedback(message):
    '''Get feedback from users'''
    bot.send_chat_action(message.chat.id, 'typing')
    log(message)
    if message.text == '/cancel':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_ru
        else:
            markup = buttons.markup_en
        cancel(message, markup)

    else:
        bot.send_message(
            config.ZWEEL, f'🆔 <a href="tg://user?id={message.from_user.id}">{message.from_user.id}</a>:', disable_notification=True)
        bot.forward_message(config.ZWEEL, message.chat.id, message.message_id)

        if not config.TEST_MODE:
            bot.send_message(
                config.AQ, f'🆔 <a href="tg://user?id={message.from_user.id}">{message.from_user.id}</a>:', disable_notification=True)
            bot.forward_message(config.AQ, message.chat.id, message.message_id)

        if message.from_user.language_code in CIS_lang_codes:
            text = 'Отлично! Ваше сообщение отправлено.'
            markup = buttons.markup_ru
        else:
            text = 'Awesome! Your message has been sent.'
            markup = buttons.markup_en

        bot.send_message(message.chat.id, text,
                         reply_to_message_id=message.message_id, reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    '''/help message'''
    if message.chat.type == 'private':
        bot.send_chat_action(message.chat.id, 'typing')
        log(message)
        if message.from_user.language_code in CIS_lang_codes:
            text = strings.cmdHelp_ru
            markup = buttons.markup_ru
        else:
            text = strings.cmdHelp_en
            markup = buttons.markup_en
        bot.send_message(message.chat.id, text, reply_markup=markup)
    else:
        pmOnly(message)


@bot.message_handler(commands=['delkey'])
def delete_keyboard(message):
    bot.delete_message(message.chat.id, message.message_id)
    msg = bot.send_message(message.chat.id, '👍',
                           reply_markup=buttons.markup_del)
    time.sleep(10)
    bot.delete_message(msg.chat.id, msg.message_id)


@bot.message_handler(commands=['ban'])
def ban(message):
    if message.chat.id == config.CSGOBETACHAT:
        if message.from_user.id in config.ADMIN_LIST:
            if message.reply_to_message:
                bot.kick_chat_member(message.reply_to_message.chat.id,
                                     message.reply_to_message.from_user.id, until_date=1)
                bot.send_message(message.chat.id, "{} получил VAC бан.".format(
                    message.reply_to_message.from_user.first_name), reply_to_message_id=message.reply_to_message.message_id)
        else:
            bot.send_message(message.chat.id, "Эта команда недоступна, Вы не являетесь разработчиком Valve.",
                             reply_to_message_id=message.message_id)


@bot.message_handler(commands=['unban'])
def unban(message):
    if message.chat.id == config.CSGOBETACHAT:
        if message.from_user.id in config.ADMIN_LIST:
            if message.reply_to_message:
                bot.unban_chat_member(message.reply_to_message.chat.id,
                                      message.reply_to_message.from_user.id, only_if_banned=True)
                bot.send_message(message.chat.id, "VAC бан {} был удалён.".format(
                    message.reply_to_message.from_user.first_name), reply_to_message_id=message.reply_to_message.message_id)
        else:
            bot.send_message(message.chat.id, "Эта команда недоступна, Вы не являетесь разработчиком Valve.",
                             reply_to_message_id=message.message_id)


def send_about_maintenance(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = strings.maintenance_ru
        markup = buttons.markup_ru
    else:
        text = strings.maintenance_en
        markup = buttons.markup_en
    bot.send_message(message.chat.id, text, reply_markup=markup)


### Inline-mode ###


@bot.inline_handler(lambda query: len(query.query) == 0)
def default_inline(inline_query):
    '''Inline mode'''
    log_inline(inline_query)
    try:
        status_text_en, status_text_ru = util.server_status()
        mm_stats_text_en, mm_stats_text_ru = util.mm_stats()
        devcount_text_en, devcount_text_ru = util.devcount()
        timer_text_en, timer_text_ru = util.timer()
        gameversion_text_en, gameversion_text_ru = util.gameversion()
        thumbs = ['https://telegra.ph/file/8b640b85f6d62f8ed2900.jpg', 'https://telegra.ph/file/57ba2b279c53d69d72481.jpg',
                    'https://telegra.ph/file/24b05cea99de936fd12bf.jpg', 'https://telegra.ph/file/6948255408689d2f6a472.jpg',
                    'https://telegra.ph/file/82d8df1e9f5140da70232.jpg']
        if inline_query.from_user.language_code in CIS_lang_codes:
            data = [status_text_ru, mm_stats_text_ru,
                    devcount_text_ru, timer_text_ru, gameversion_text_ru]
            titles = ['Состояние серверов', 'Статистика ММ',
                        'Бета-версия', 'Сброс ограничений', 'Версия игры']
            descriptions = ['Проверить доступность серверов', 'Посмотреть количество онлайн игроков', 'Узнать количество онлайн разработчиков',
                            'Время до сброса ограничений опыта и дропа', 'Проверить последнюю версию игры']
            markup = []
            for i in data:
                markup.append(buttons.markup_inline_button_ru)
        else:
            data = [status_text_en, mm_stats_text_en,
                    devcount_text_en, timer_text_en, gameversion_text_en]
            titles = ['Server status', 'MM stats',
                        'Beta version', 'Drop cap reset', 'Game version']
            descriptions = ['Check the availability of the servers', 'Check the count of online players', 'Show the count of in-game developers',
                            'Time left until experience and drop cap reset', 'Check the latest game version']
            markup = []
            for i in data:
                markup.append(buttons.markup_inline_button_en)
        results = []
        for data, tt, desc, thumb, inline_button in zip(data, titles, descriptions, thumbs, markup):
            results.append(types.InlineQueryResultArticle(random.randint(0, 9999), tt, input_message_content=types.InputTextMessageContent(
                data, parse_mode='html'), thumb_url=thumb, description=desc, reply_markup=inline_button))
        bot.answer_inline_query(inline_query.id, results, cache_time=5)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')


@bot.inline_handler(lambda query: validators.url(query.query) == True and query.query.startswith('https://telegra.ph/'))
def share_inline(inline_query):
    log_inline(inline_query)
    if inline_query.from_user.language_code in CIS_lang_codes:
        title = 'Ваша игровая статистика'
    else:
        title = 'Your in-game statistics'
    r = types.InlineQueryResultArticle('1', title, input_message_content=types.InputTextMessageContent(
        inline_query.query), description=inline_query.query)
    bot.answer_inline_query(inline_query.id, [r], cache_time=5)


@bot.inline_handler(lambda query: len(query.query) >= 0)
def inline_dc(inline_query):
    log_inline(inline_query)
    try:
        eu_north_text_en, eu_north_text_ru = datacenters.eu_north()
        eu_east_text_en, eu_east_text_ru = datacenters.eu_east()
        eu_west_text_en, eu_west_text_ru = datacenters.eu_west()
        usa_north_text_en, usa_north_text_ru = datacenters.usa_north()
        usa_south_text_en, usa_south_text_ru = datacenters.usa_south()
        china_text_en, china_text_ru = datacenters.china()
        emirates_text_en, emirates_text_ru = datacenters.emirates()
        hong_kong_text_en, hong_kong_text_ru = datacenters.hong_kong()
        india_text_en, india_text_ru = datacenters.india()
        japan_text_en, japan_text_ru = datacenters.japan()
        singapore_text_en, singapore_text_ru = datacenters.singapore()
        south_korea_text_en, south_korea_text_ru = datacenters.south_korea()
        australia_text_en, australia_text_ru = datacenters.australia()
        africa_text_en, africa_text_ru = datacenters.africa()
        south_america_text_en, south_america_text_ru = datacenters.south_america()
        thumbs = ['https://telegra.ph/file/ff0dad30ae32144d7cd0c.jpg', 'https://telegra.ph/file/1de1e51e62b79cae5181a.jpg', 'https://telegra.ph/file/0b209e65c421910419f34.jpg',
                    'https://telegra.ph/file/b2213992b750940113b69.jpg', 'https://telegra.ph/file/11b6601a3e60940d59c88.jpg', 'https://telegra.ph/file/1c2121ceec5d1482173d5.jpg',
                    'https://telegra.ph/file/2265e9728d06632773537.png', 'https://telegra.ph/file/4d269cb98aadaae391024.jpg', 'https://telegra.ph/file/4d269cb98aadaae391024.jpg',
                    'https://telegra.ph/file/4d269cb98aadaae391024.jpg', 'https://telegra.ph/file/06119c30872031d1047d0.jpg', 'https://telegra.ph/file/06119c30872031d1047d0.jpg',
                    'https://telegra.ph/file/5dc6beef1556ea852284c.jpg', 'https://telegra.ph/file/12628c8193b48302722e8.jpg', 'https://telegra.ph/file/60f8226ea5d72815bef57.jpg']
        tagList = [tags.chinese, tags.emirati, tags.hong_kongese, tags.indian, tags.japanese,
                    tags.singaporean, tags.south_korean, tags.north_european, tags.east_european, tags.west_european,
                    tags.northern_usa, tags.southern_usa, tags.australian, tags.african, tags.south_american]
        if inline_query.from_user.language_code in CIS_lang_codes:
            data = [china_text_ru, emirates_text_ru, hong_kong_text_ru, india_text_ru, japan_text_ru, singapore_text_ru, south_korea_text_ru, eu_north_text_ru,
                    eu_east_text_ru, eu_west_text_ru, usa_north_text_ru, usa_south_text_ru, australia_text_ru, africa_text_ru, south_america_text_ru]
            titles = ['Китайские ДЦ', 'Эмиратский ДЦ', 'Гонконгский ДЦ', 'Индийские ДЦ', 'Японский ДЦ', 'Сингапурский ДЦ', 'Южнокорейский ДЦ', 'Североевропейский ДЦ',
                        'Восточноевропейские ДЦ', 'Западноевропейские ДЦ', 'ДЦ северной части США', 'ДЦ южной части США', 'Австралийский ДЦ',
                        'Африканский ДЦ', 'Южноамериканские ДЦ']
            descriptions = ['Проверить состояние']
            markup = []
            for i in data:
                markup.append(buttons.markup_inline_button_ru)
        else:
            data = [china_text_en, emirates_text_en, hong_kong_text_en, india_text_en, japan_text_en, singapore_text_en, south_korea_text_en, eu_north_text_en,
                    eu_east_text_en, eu_west_text_en, usa_north_text_en, usa_south_text_en, australia_text_en, africa_text_en, south_america_text_en]
            titles = ['Chinese DC', 'Emirati DC', 'Hong Kongese DC', 'Indian DC', 'Japanese DC', 'Singaporean DC', 'South Korean DC', 'North European DC',
                        'East European DC', 'West European DC', 'Northern USA DC', 'Southern USA DC', 'Australian DC', 'African DC', 'South American DC']
            descriptions = ['Check the status']
            markup = []
            for i in data:
                markup.append(buttons.markup_inline_button_en)
        results = []
        for data, tt, desc, thumb, dctag, inline_markup in zip(data, titles, descriptions*100, thumbs, tagList, markup):
            for id in dctag:
                if inline_query.query == id:
                    results.append(types.InlineQueryResultArticle(random.randint(0, 9999), tt, input_message_content=types.InputTextMessageContent(
                        data, parse_mode='html'), thumb_url=thumb, description=desc, reply_markup=inline_markup))
        bot.answer_inline_query(inline_query.id, results, cache_time=5)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')


###


@bot.message_handler(content_types=['text'])
def answer(message):
    try:
        if message.chat.type == 'private':
            log(message)
            data = pd.read_csv(config.USER_DB_FILE_PATH)
            if not data['UserID'].isin([message.from_user.id]).any():
                new_data = pd.DataFrame([[message.from_user.first_name, message.from_user.id,
                                        message.from_user.language_code]], columns=['Name', 'UserID', 'Language'])
                pd.concat([data, new_data]).to_csv(
                    config.USER_DB_FILE_PATH, index=False)

            if message.text.lower() == 'server statistics' or message.text.lower() == 'статистика серверов':
                server_stats(message)

            elif message.text.lower() == 'extra features' or message.text.lower() == 'дополнительные функции':
                extra_features(message)

            elif message.text.lower() == 'profile information' or message.text.lower() == 'информация о профиле':
                profile_info(message)

            else:
                unknown_request(message)

        else:
            if message.from_user.id == 777000:
                if message.forward_from_chat.id == config.CSGOBETACHANNEL and 'Обновлены файлы локализации' in message.text:
                    bot.send_sticker(
                        config.CSGOBETACHAT, 'CAACAgIAAxkBAAID-l_9tlLJhZQSgqsMUAvLv0r8qhxSAAIKAwAC-p_xGJ-m4XRqvoOzHgQ', reply_to_message_id=message.message_id)

    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')


### Misc ###


def log(message):
    '''The bot sends log to log channel'''
    text = f"""✍️ User: <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
ID: {message.from_user.id}
Language: {message.from_user.language_code}
Private message: {message.text}
"""
    if not config.TEST_MODE:
        bot.send_message(config.LOGCHANNEL, text, parse_mode='html')


def log_inline(inline_query):
    '''The bot sends inline query to log channel'''
    text = f"""🛰 User: <a href="tg://user?id={inline_query.from_user.id}">{inline_query.from_user.first_name}</a>
ID: {inline_query.from_user.id}
Language: {inline_query.from_user.language_code}
Inline query: {inline_query.query}
"""
    if not config.TEST_MODE:
        bot.send_message(config.LOGCHANNEL, text, parse_mode='html')


bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.infinity_polling()
