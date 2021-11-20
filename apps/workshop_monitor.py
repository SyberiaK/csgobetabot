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
from addons import strings


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
                        time.sleep(45)
                        continue

                    delta = list(zip(mapNames, newIDS))
                    if len(delta) < 2:
                        for x, y in delta:
                            text = strings.notiNewMap_ru.format(x, y)
                    else:
                        names = ' и '.join(
                            [', '.join(mapNames[:-1]), mapNames[-1]] if len(mapNames) > 2 else mapNames)
                        text = strings.notiNewMaps_ru.format(names)
                    send_alert(text)
                    initialIDs = rerunIDs

                time.sleep(45)


def send_alert(text):
    bot = telebot.TeleBot(config.BOT_TOKEN)

    if not config.TEST_MODE:
        chat_list = [config.CSGOBETACHAT, config.CSGONOTIFY]
    else:
        chat_list = [config.AQ]

    for chatID in chat_list:
        msg = bot.send_message(chatID, text, parse_mode='html')
        if chatID == config.CSGOBETACHAT:
            bot.pin_chat_message(msg.chat.id, msg.id,
                                 disable_notification=True)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s | %(message)s', datefmt='%H:%M:%S — %d/%m/%Y')
    workshop_monitor()
