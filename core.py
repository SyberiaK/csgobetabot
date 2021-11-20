import logging
import telebot
import time
from threading import Thread


import config
from addons import strings
from addons import file_manager
from apps.valve_api import ValveServersAPI
from apps.web import PeakOnline, Monthly


api = ValveServersAPI()
peak_count = PeakOnline()
month_unique = Monthly()


def info_updater():
    while True:
        try:
            print('\nNew session started..\n')
            cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)

            cache_key_list = []
            cache_value_list = []
            value_list = []

            playerCount = api.get_players()
            devCount = api.get_devs()
            overallData = api.get_status()

            for keys, values in cacheFile.items():
                cache_key_list.append(keys)
                cache_value_list.append(values)

            for data in [cacheFile['public_build_ID'], cacheFile['dpr_build_ID'], cacheFile['game_coordinator']]:
                value_list.append(data)
            for data in overallData[0:9]:
                value_list.append(data)
            for data in [playerCount, devCount, cacheFile['dev_all_time_peak'], peak_count.get_peak(), cacheFile['peak_all_time'], cacheFile['unique_monthly']]:
                value_list.append(data)
            for data in [cacheFile['client_version'], cacheFile['server_version'], cacheFile['patch_version'], cacheFile['version_timestamp']]:
                value_list.append(data)
            for data in [cacheFile['graph_url'], cacheFile['graph_url2']]:
                value_list.append(data)
            for data in overallData[9:10]:
                value_list.append(data)

            for values, cache_values, cache_keys in zip(value_list, cache_value_list, cache_key_list):
                if values != cache_values:
                    file_manager.updateJson(
                        config.CACHE_FILE_PATH, values, cache_keys)

            if playerCount > cacheFile['peak_all_time']:
                file_manager.updateJson(
                    config.CACHE_FILE_PATH, playerCount, cache_key_list[16])
                send_alert(playerCount, cache_key_list[16])

            if devCount > cacheFile['dev_all_time_peak']:
                file_manager.updateJson(
                    config.CACHE_FILE_PATH, devCount, cache_key_list[14])
                send_alert(devCount, cache_key_list[14])

            time.sleep(40)

        except Exception as e:
            print(f'\n> Error in the main thread:\n\n{e}\n')


def unique_monthly():
    while True:
            print('\nChecking monthly unique players..\n')

            try:
                newValue = month_unique.get_unique()
            except Exception as e:
                print(f'\n> Error while gathering monthly players:\n\n{e}\n')
                time.sleep(45)
                continue

            cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
            uniqueMonthly = cacheFile['unique_monthly']

            if newValue != uniqueMonthly:
                file_manager.updateJson(
                    config.CACHE_FILE_PATH, newValue, 'unique_monthly')

            time.sleep(86400)


def send_alert(newVal, key):
    bot = telebot.TeleBot(config.BOT_TOKEN)
    if key == 'dev_all_time_peak':
        text = strings.notiNewDevPeak_ru.format(newVal)
    else:
        text = strings.notiNewPlayerPeak_ru.format(newVal)

    if not config.TEST_MODE:
        chat_list = [config.CSGOBETACHAT, config.AQ]
    else:
        chat_list = [config.AQ]

    for chatID in chat_list:
        msg = bot.send_message(chatID, text, parse_mode='html')
        if chatID != config.AQ:
            bot.pin_chat_message(msg.chat.id, msg.id,
                                 disable_notification=True)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s | %(threadName)s: %(message)s', datefmt='%H:%M:%S — %d/%m/%Y')

    t1 = Thread(target = unique_monthly)
    t2 = Thread(target = info_updater)

    t1.start()
    t2.start()
