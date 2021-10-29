import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


import logging
import requests
import time 
import telebot


import config
from plugins import strings


API = f'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1?appid={config.CSGO_BETA_APP_ID}'


def tracker():
    while True:
        try:
            current_dev_count = requests.get(
                API).json()["response"]["player_count"]
        except Exception as e:
            print(f'\n> Initial run error:\n\n{e}\n')
            time.sleep(45)
            continue

        while True:
            try:
                new_dev_count = requests.get(
                    API).json()["response"]["player_count"]
            except Exception as e:
                print(f'\n> Second run error:\n\n{e}\n')
                time.sleep(45)
                continue

            if new_dev_count != current_dev_count:
                send_alert(current_dev_count, new_dev_count)
                current_dev_count = new_dev_count
            time.sleep(45)

def send_alert(oldVal, newVal):
    bot = telebot.TeleBot(config.BOT_TOKEN)
    bot.send_message(config.CSGODEVTRACKER, strings.dev_change_text.format(
        oldVal, newVal), parse_mode='html')

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s | %(message)s', datefmt='%H:%M:%S — %d/%m/%Y')
    tracker()