import logging
import time
from datetime import datetime, timedelta
from threading import Thread

import pandas as pd
import telebot

import config
from addons import file_manager
from apps.valve_api import ValveServersAPI
from apps.web import Currency, Monthly
from strings import notifications

api = ValveServersAPI()
month_unique = Monthly()
currency = Currency()


def info_updater():
    while True:
        try:
            print("\nNew session started..\n")
            cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)

            overallData = api.get_status()

            for key, value in overallData.items():
                for cachedKey, cachedValue in cacheFile.items():
                    if key == cachedKey:
                        if value != cachedValue:
                            file_manager.updateJson(config.CACHE_FILE_PATH, value, key)

            if cacheFile["online_players"] > cacheFile["player_alltime_peak"]:
                file_manager.updateJson(
                    config.CACHE_FILE_PATH, cacheFile["online_players"], "player_alltime_peak"
                )
                send_alert(cacheFile["online_players"], "online_players")

            df = pd.read_csv(config.PLAYER_CHART_FILE_PATH, parse_dates=["DateTime"])
            end_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            start_date = (datetime.utcnow() - timedelta(days=1)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            mask = (df["DateTime"] > start_date) & (df["DateTime"] <= end_date)
            player_24h_peak = int(df.loc[mask]["Players"].max())

            if player_24h_peak != cacheFile["player_24h_peak"]:
                file_manager.updateJson(
                    config.CACHE_FILE_PATH,
                    player_24h_peak,
                    "player_24h_peak",
                )

            time.sleep(40)

        except Exception as e:
            print(f"\n> Error in the main thread:\n\n{e}\n")
            time.sleep(40)


def unique_monthly():
    while True:
        print("\nChecking monthly unique players..\n")

        try:
            data = month_unique.get_unique()
        except Exception as e:
            print(f"\n> Error while gathering monthly players:\n\n{e}\n")
            time.sleep(45)
            continue

        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)

        if data["monthly_unique_players"] != cacheFile["monthly_unique_players"]:
            send_alert([cacheFile["monthly_unique_players"], data["monthly_unique_players"]], "monthly_unique_players")
            file_manager.updateJson(
                config.CACHE_FILE_PATH,
                data["monthly_unique_players"],
                "monthly_unique_players",
            )

        time.sleep(86400)


def check_currency():
    while True:
        print("\nChecking key price..\n")

        try:
            newValue = currency.get_currency()
        except Exception as e:
            print(f"\n> Error while gathering key price:\n\n{e}\n")
            time.sleep(45)
            continue

        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        prices = cacheFile["key_price"]

        if newValue != prices:
            file_manager.updateJson(config.CACHE_FILE_PATH, newValue, "key_price")

        time.sleep(86400)


def send_alert(newVal, key):
    bot = telebot.TeleBot(config.BOT_TOKEN)
    if key == "online_players":
        text = notifications.playersPeak.format(newVal)
    else:
        text = notifications.monthlyUnique.format(newVal[0], newVal[1])

    if not config.TEST_MODE:
        chat_list = [config.INCS2CHAT, config.AQ]
    else:
        chat_list = [config.AQ]

    for chatID in chat_list:
        msg = bot.send_message(chatID, text, parse_mode="html")
        if chatID != config.AQ:
            bot.pin_chat_message(msg.chat.id, msg.id, disable_notification=True)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(threadName)s: %(message)s",
        datefmt="%H:%M:%S — %d/%m/%Y",
    )

    t1 = Thread(target=info_updater)
    t2 = Thread(target=unique_monthly)
    t3 = Thread(target=check_currency)

    t1.start()
    t2.start()
    t3.start()
