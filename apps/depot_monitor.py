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
from steam.enums import EResult
from steam.client import SteamClient


import config
from apps import file_manager
from plugins import strings


logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s | %(name)s: %(message)s', datefmt='%H:%M:%S — %d/%m/%Y')


client = SteamClient()
client.set_credential_location("./csgobetabot/data/creds/")


@client.on("error")
def handle_error(result):
    print(f"\n> Logon result: {repr(result)}\n")


@client.on("channel_secured")
def send_login():
    if client.relogin_available:
        client.relogin()


@client.on("connected")
def handle_connected():
    print(f"\n> Connected to {client.current_server_addr}\n")


@client.on("reconnect")
def handle_reconnect(delay):
    print(f"\n> Reconnect in {delay}s...\n")


@client.on("disconnected")
def handle_disconnect():
    print("\n> Disconnected.\n")

    if client.relogin_available:
        print("\n> Reconnecting...\n")
        client.reconnect(maxdelay=30)


@client.on("logged_on")
def handle_after_logon():
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
    if key == 'public_build_ID':
        text = strings.notificationTextUPD.format(newVal)
    elif key == 'dpr_build_ID':
        text = strings.notificationTextDPR.format(newVal)
    elif key == 'rkvtest':
        text = strings.rkvTextUPD.format(newVal)
    elif key == 'test':
        text = strings.testTextUPD.format(newVal)

    bot = telebot.TeleBot(config.BOT_TOKEN)
    if not config.TEST_MODE:
        chat_list = [config.CSGOBETACHAT, config.CSGONOTIFY, config.AQ]
    else:
        chat_list = [config.AQ]

    for chatID in chat_list:
        msg = bot.send_message(
            chatID, text, parse_mode='html', disable_web_page_preview=True)
        if chatID == config.CSGOBETACHAT:
            bot.pin_chat_message(msg.chat.id, msg.id,
                                 disable_notification=True)


try:
    result = client.login(username=config.STEAM_USERNAME,
                     password=config.STEAM_PASS)

    if result != EResult.OK:
        print(f"\n> Failed to login: {repr(result)}\n")
        raise SystemExit

    client.run_forever()
except KeyboardInterrupt:
    if client.connected:
        print("\n> Logout\n")
        client.logout()
