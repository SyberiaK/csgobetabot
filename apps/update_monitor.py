import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


import time
import logging
import telebot
from steam.client import SteamClient


import config
from apps import file_manager
from plugins import strings


def setup():
    client = SteamClient()
    try:
        client.login(username=config.STEAM_USERNAME,
                     password=config.STEAM_PASS)

        check_for_updates(client)
    except Exception as e:
        print(f' - Error:\n{e}\n\n\n')


def check_for_updates(client):
    while True:
        try:
            for keys, values in client.get_product_info(apps=[730], timeout=15).items():
                for k, v in values.items():
                    currentPublicBuild = v['depots']['branches']['public']['buildid']
                    currentDPRBuild = v['depots']['branches']['dpr']['buildid']
                    try:
                        currentRKVBuild = v['depots']['branches']['rkvtest']['buildid']
                    except Exception as e:
                        print(f' - Error:\n{e}\n\n\n')
                    try:
                        currentTestBuild = v['depots']['branches']['test']['buildid']
                    except Exception as e:
                        print(f' - Error:\n{e}\n\n\n')

            cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
            cache_key_list = []
            for keys, values in cacheFile.items():
                cache_key_list.append(keys)

            if currentPublicBuild != cacheFile['public_build_ID']:
                file_manager.updateJson(
                    config.CACHE_FILE_PATH, currentPublicBuild, cache_key_list[0])
                send_alert(currentPublicBuild, cache_key_list[0])

            if currentDPRBuild != cacheFile['dpr_build_ID']:
                file_manager.updateJson(
                    config.CACHE_FILE_PATH, currentDPRBuild, cache_key_list[1])
                send_alert(currentDPRBuild, cache_key_list[1])

            if currentRKVBuild != cacheFile['rkvtest']:
                file_manager.updateJson(
                    config.CACHE_FILE_PATH, currentRKVBuild, cache_key_list[25])
                send_alert(currentRKVBuild, cache_key_list[25])

            if currentTestBuild != cacheFile['test']:
                file_manager.updateJson(
                    config.CACHE_FILE_PATH, currentTestBuild, cache_key_list[26])
                send_alert(currentTestBuild, cache_key_list[26])

            time.sleep(10)

        except Exception as e:
            print(f' - Error:\n{e}\n\n\n')


def send_alert(newVal, key):
    bot = telebot.TeleBot(config.BOT_TOKEN)
    if key == 'public_build_ID':
        text_ru = strings.notiNewBuild_ru.format(newVal)
        text_en = strings.notiNewBuild_en.format(newVal)
        notify_text = strings.notificationTextUPD.format(newVal)
    elif key == 'dpr_build_ID':
        text_ru = strings.notiNewDPRBuild_ru.format(newVal)
        text_en = strings.notiNewDPRBuild_en.format(newVal)
        notify_text = strings.notificationTextDPR.format(newVal)
    elif key == 'rkvtest':
        text_ru = strings.rkvTextUPD.format(newVal)
    elif key == 'test':
        text_ru = strings.testTextUPD.format(newVal)

    if not config.TEST_MODE:
        chat_list = [config.CSGOBETACHAT,
                     config.CSGOBETACHAT_EN, config.CSGONOTIFY, config.AQ]
        nonpin = [config.CSGONOTIFY, config.AQ]
        testpurposes = ['rkvtest', 'test']
    else:
        chat_list = [config.AQ]
    for chatID in chat_list:
        if chatID == config.CSGOBETACHAT:
            msg = bot.send_message(chatID, text_ru, parse_mode='html')
        elif chatID == config.CSGONOTIFY:
            if key not in testpurposes:
                msg = bot.send_message(chatID, notify_text, parse_mode='html')
        else:
            if key not in testpurposes:
                msg = bot.send_message(chatID, text_en, parse_mode='html')
        if chatID not in nonpin:
            bot.pin_chat_message(msg.chat.id, msg.id,
                                 disable_notification=True)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s %(name)s: %(message)s', datefmt='%H:%M:%S — %d/%m/%Y')
    setup()
