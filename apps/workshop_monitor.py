import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


import requests
import logging
import telebot
import time
import re


import config
from plugins import strings


workshop_url = f'https://api.steampowered.com/IPublishedFileService/GetUserFiles/v1/?key={config.STEAM_API_KEY}&steamid={config.CSGO_STEAM_PROFILE_ID}&appid={config.CSGO_APP_ID}&page=1&numperpage=18'
pattern = r' \[.*?\]'


def workshop_monitor():
    while True:
        try:
            initialData = requests.get(workshop_url).json()[
                'response']['publishedfiledetails']
            initialIDs = []
            for map in initialData:
                initialIDs.append(map['publishedfileid'])

        except Exception as e:
            print(f'\n> Initial run error:\n\n{e}\n')
            time.sleep(45)
            continue

        if len(initialIDs) == 18:
            while True:
                try:
                    rerunData = requests.get(workshop_url).json()[
                        'response']['publishedfiledetails']
                    rerunIDs = []
                    for map in rerunData:
                        rerunIDs.append(map['publishedfileid'])

                except Exception as e:
                    print(f'\n> Second run error:\n\n{e}\n')
                    time.sleep(45)
                    continue

                if len(rerunIDs) == 18 and rerunIDs != initialIDs:
                    dump = initialIDs[:]
                    newIDS = [
                        i for i in rerunIDs if not i in dump or dump.remove(i)]

                    try:
                        mapNames = []
                        for id in newIDS:
                            name = list(filter(lambda x: x['publishedfileid'] == id, rerunData))[
                                0]['title']
                            cleanName = re.sub(pattern, '', name)
                            mapNames.append(cleanName)

                    except Exception as e:
                        print(f'\n> Map name error:\n\n{e}\n')
                        continue

                    delta = list(zip(mapNames, newIDS))
                    if len(delta) < 2:
                        for x, y in delta:
                            text_ru = strings.notiNewMap_ru.format(x, y)
                            text_en = strings.notiNewMap_en.format(x, y)
                    else:
                        names = ' и '.join(
                            [', '.join(mapNames[:-1]), mapNames[-1]] if len(mapNames) > 2 else mapNames)
                        names_en = ' and '.join(
                            [', '.join(mapNames[:-1]), mapNames[-1]] if len(mapNames) > 2 else mapNames)
                        text_ru = strings.notiNewMaps_ru.format(names)
                        text_en = strings.notiNewMaps_en.format(names_en)
                    send_alert(text_ru, text_en)
                    initialIDs = rerunIDs


def send_alert(text_ru, text_en):
    bot = telebot.TeleBot(config.BOT_TOKEN)
    if not config.TEST_MODE:
        chat_list = [config.CSGOBETACHAT,
                     config.CSGOBETACHAT_EN, config.CSGONOTIFY, config.AQ]
        nonpin = [config.CSGONOTIFY, config.AQ]
    else:
        chat_list = [config.AQ]
    for chatID in chat_list:
        if chatID == config.CSGOBETACHAT_EN:
            msg = bot.send_message(chatID, text_en, parse_mode='html')
        else:
            msg = bot.send_message(chatID, text_ru, parse_mode='html')
        if chatID not in nonpin:
            bot.pin_chat_message(msg.chat.id, msg.id,
                                 disable_notification=True)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%H:%M:%S — %d/%m/%Y')
    workshop_monitor()
