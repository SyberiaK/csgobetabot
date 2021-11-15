import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import gevent.monkey
gevent.monkey.patch_all()


import time
import logging
from threading import Thread
from steam.enums import EResult
from steam.client import SteamClient
from csgo.client import CSGOClient
import telebot


import config
import file_manager
from scrapper import GameVersion
from plugins import strings


logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s | %(threadName)s | %(name)s: %(message)s', datefmt='%H:%M:%S — %d/%m/%Y')


client = SteamClient()
client.set_credential_location(config.STEAM_CREDS_PATH)
cs = CSGOClient(client)
gv = GameVersion()


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


@cs.on('connection_status')
def gc_ready(status):
    if status == 0:
        game_coordinator = 'normal'
    elif status == 1:
        game_coordinator = 'internal server error'
    elif status == 2:
        game_coordinator = 'internal bot error'
    elif status == 3:
        game_coordinator = 'reloading'
    elif status == 4:
        game_coordinator = 'internal Steam error'
    else:
        game_coordinator = 'N/A'

    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    cache_key_list = []
    for keys, values in cacheFile.items():
        cache_key_list.append(keys)

    if game_coordinator != cacheFile['game_coordinator']:
        file_manager.updateJson(
            config.CACHE_FILE_PATH, game_coordinator, cache_key_list[2])


@client.on("logged_on")
def handle_after_logon():
    t1.start()
    t2.start()


def depots():
    while True:
        try:
            for keys, values in client.get_product_info(apps=[730], timeout=15).items():
                for k, v in values.items():
                    currentPublicBuild = v['depots']['branches']['public']['buildid']
                    currentDPRBuild = v['depots']['branches']['dpr']['buildid']
                    try:
                        currentRKVBuild = v['depots']['branches']['rkvtest']['buildid']
                    except Exception as e:
                        print(f'\n> Error fetching RKV build:\n\n{e}\n')
                    try:
                        currentTestBuild = v['depots']['branches']['test']['buildid']
                    except Exception as e:
                        print(f'\n> Error fetching Test build:\n\n{e}\n')

        except Exception as e:
            print(f'\n> Error trying to fetch depots:\n\n{e}\n')
            time.sleep(45)
            continue

        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        cache_key_list = []
        for keys, values in cacheFile.items():
            cache_key_list.append(keys)

        if currentPublicBuild != cacheFile['public_build_ID']:
            file_manager.updateJson(
                config.CACHE_FILE_PATH, currentPublicBuild, cache_key_list[0])
            send_alert(currentPublicBuild, cache_key_list[0])
            t4 = Thread(target = gv_updater)
            t4.start()

        if currentDPRBuild != cacheFile['dpr_build_ID']:
            file_manager.updateJson(
                config.CACHE_FILE_PATH, currentDPRBuild, cache_key_list[1])
            send_alert(currentDPRBuild, cache_key_list[1])
            t3 = Thread(target = ds)
            t3.start()

        if currentRKVBuild != cacheFile['rkvtest']:
            file_manager.updateJson(
                config.CACHE_FILE_PATH, currentRKVBuild, cache_key_list[25])
            send_alert(currentRKVBuild, cache_key_list[25])

        if currentTestBuild != cacheFile['test']:
            file_manager.updateJson(
                config.CACHE_FILE_PATH, currentTestBuild, cache_key_list[26])
            send_alert(currentTestBuild, cache_key_list[26])

        time.sleep(45)


def gc():
    cs.launch()


def ds():
    timeout = time.time() + 60*90
    while True:
        try:
            for keys, values in client.get_product_info(apps=[741], timeout=15).items():
                for k, v in values.items():
                    currentDSchangenumber = v['_change_number']

        except Exception as e:
            print(f'\n> First DS run error:\n\n{e}\n')
            time.sleep(45)
            continue

        while True:
            try:
                for keys, values in client.get_product_info(apps=[741], timeout=15).items():
                    for k, v in values.items():
                        newDSchangenumber = v['_change_number']

            except Exception as e:
                print(f'\n> Second DS run error:\n\n{e}\n')
                time.sleep(45)
                continue

            if newDSchangenumber != currentDSchangenumber:
                send_alert(newDSchangenumber, 'ds')
                sys.exit()

            elif time.time() > timeout:
                sys.exit()

            time.sleep(45)


def gv_updater():
    while True:
        try:
            newValue = gv.get_gameVer()

        except Exception as e:
            print(f'\n> Error trying to get new version:\n\n{e}\n')
            time.sleep(45)
            continue

        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        oldVersion = cacheFile['client_version']
        keyList = ['client_version', 'server_version', 'patch_version', 'version_timestamp']

        if newValue[0] != oldVersion:
            for val, key in zip(newValue, keyList):
                file_manager.updateJson(
                    config.CACHE_FILE_PATH, val, key)
            sys.exit()

        time.sleep(45)

def send_alert(newVal, key):
    if key == 'public_build_ID':
        text = strings.notificationTextUPD.format(newVal)
    elif key == 'dpr_build_ID':
        text = strings.notificationTextDPR.format(newVal)
    elif key == 'rkvtest':
        text = strings.notificationTextRKV.format(newVal)
    elif key == 'test':
        text = strings.notificationTextTST.format(newVal)
    elif key == 'ds':
        text = strings.notificationTextDS.format(newVal)

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


t1 = Thread(target = depots)
t2 = Thread(target = gc)

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
