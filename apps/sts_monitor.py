import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


import time
import re
import telebot
import logging
import feedparser


import config
from plugins import strings


stsgroup_url = 'https://steamcommunity.com/groups/STSLounge/rss/'


def sts_monitor():
    while True:
        try:
            currentSTS = feedparser.parse(stsgroup_url).entries
            latestPost0, latestPost1, latestPost2 = currentSTS[
                0].link, currentSTS[1].link, currentSTS[2].link
            latestPosts = [latestPost0, latestPost1, latestPost2]

        except Exception as e:
            print(f'\n> First run error:\n\n{e}\n')
            time.sleep(45)
            continue

        if len(latestPosts) != 0:
            while True:
                try:
                    newSTS = feedparser.parse(stsgroup_url).entries
                    newPost0, newPost1, newPost2 = newSTS[0].link, newSTS[1].link, newSTS[2].link
                    newPosts = [newPost0, newPost1, newPost2]

                except Exception as e:
                    print(f'\n> Second run error:\n\n{e}\n')
                    time.sleep(45)
                    continue

                if len(newPosts) != 0:
                    if newPosts != latestPosts:
                        if newPost0 != latestPost0:
                            if 'csgo' in newSTS[0].summary_detail.value:
                                newStrings = newSTS[0]
                                strList = re.findall(
                                    r'csgo/[\w]+\.txt', newStrings.summary_detail.value)
                                cleanList = []
                                for i in strList:
                                    cleanList.append(
                                        re.sub(r'csgo/', '', i))
                                changes = '• ' + '\n• '.join(cleanList)
                                numberOfChanges = re.findall(
                                    r'\d+', newStrings.title)
                                numberOfChanges = numberOfChanges[0]
                                latestPosts = newPosts
                                send_alert(
                                    changes, numberOfChanges, newStrings.link)
                time.sleep(45)


def send_alert(data, value, link):
    text = strings.notiNewSTS_ru.format(value, data, link)

    bot = telebot.TeleBot(config.BOT_TOKEN)
    if not config.TEST_MODE:
        chatID = config.CSGOBETACHAT
    else:
        chatID = config.AQ

    msg = bot.send_message(
        chatID, text, parse_mode='html', disable_web_page_preview=True)
    bot.pin_chat_message(msg.chat.id, msg.id,
                            disable_notification=True)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s | %(message)s', datefmt='%H:%M:%S — %d/%m/%Y')
    sts_monitor()
