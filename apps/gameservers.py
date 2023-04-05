import env
import gevent.monkey

gevent.monkey.patch_all()

import logging
import time
from threading import Thread

import config
import telebot
from addons import file_manager
from csgo.client import CSGOClient
from steam.client import SteamClient
from steam.enums import EResult
from strings import notifications
from web import GameVersion

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(threadName)s | %(name)s: %(message)s",
    datefmt="%H:%M:%S — %d/%m/%Y",
)


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


@cs.on("connection_status")
def gc_ready(status):
    if status == 0:
        game_coordinator = "normal"
    elif status == 1:
        game_coordinator = "internal server error"
    elif status == 2:
        game_coordinator = "offline"
    elif status == 3:
        game_coordinator = "reloading"
    elif status == 4:
        game_coordinator = "internal Steam error"
    else:
        game_coordinator = "unknown"

    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)

    if game_coordinator != cacheFile["game_coordinator"]:
        file_manager.updateJson(
            config.CACHE_FILE_PATH, game_coordinator, "game_coordinator"
        )


@client.on("logged_on")
def handle_after_logon():
    t1 = Thread(target=depots)
    t1.start()
    t2 = Thread(target=gc)
    t2.start()
    t3 = Thread(target=online_players)
    t3.start()


def depots():
    while True:
        try:
            for keys, values in client.get_product_info(apps=[740], timeout=15).items():
                for k, v in values.items():
                    DSBuildID = int(v["depots"]["branches"]["public"]["buildid"])

            for keys, values in client.get_product_info(apps=[741], timeout=15).items():
                for k, v in values.items():
                    ValveDSChangeNumber = v["_change_number"]

            for keys, values in client.get_product_info(apps=[745], timeout=15).items():
                for k, v in values.items():
                    SDKBuildID = int(v["depots"]["branches"]["public"]["buildid"])

            for keys, values in client.get_product_info(apps=[730], timeout=15).items():
                for k, v in values.items():
                    DPRBuildID = int(v["depots"]["branches"]["dpr"]["buildid"])
                    DPRPBuildID = int(v["depots"]["branches"]["dprp"]["buildid"])
                    PublicBuildID = int(v["depots"]["branches"]["public"]["buildid"])

        except Exception as e:
            print(f"\n> Error trying to fetch depots:\n\n{e}\n")
            time.sleep(45)
            continue

        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)

        if SDKBuildID != cacheFile["sdk_build_id"]:
            file_manager.updateJson(config.CACHE_FILE_PATH, SDKBuildID, "sdk_build_id")
            send_alert(SDKBuildID, "sdk_build_id")

        if DSBuildID != cacheFile["ds_build_id"]:
            file_manager.updateJson(config.CACHE_FILE_PATH, DSBuildID, "ds_build_id")
            send_alert(DSBuildID, "ds_build_id")

        if ValveDSChangeNumber != cacheFile["valve_ds_changenumber"]:
            file_manager.updateJson(
                config.CACHE_FILE_PATH, ValveDSChangeNumber, "valve_ds_changenumber"
            )
            send_alert(ValveDSChangeNumber, "valve_ds_changenumber")

        if DPRPBuildID != cacheFile["dprp_build_id"]:
            file_manager.updateJson(config.CACHE_FILE_PATH, DPRPBuildID, "dprp_build_id")
            send_alert(DPRPBuildID, "dprp_build_id")

        if DPRBuildID != cacheFile["dpr_build_id"]:
            file_manager.updateJson(config.CACHE_FILE_PATH, DPRBuildID, "dpr_build_id")
            if DPRBuildID == cacheFile["public_build_id"]:
                send_alert(DPRBuildID, "dpr_build_sync_id")
            else:
                send_alert(DPRBuildID, "dpr_build_id")

        if PublicBuildID != cacheFile["public_build_id"]:
            file_manager.updateJson(
                config.CACHE_FILE_PATH, PublicBuildID, "public_build_id"
            )
            send_alert(PublicBuildID, "public_build_id")
            t3 = Thread(target=gv_updater)
            t3.start()

        time.sleep(45)


def gc():
    cs.launch()


def gv_updater():
    while True:
        try:
            data = gv.get_gameVer()

        except Exception as e:
            print(f"\n> Error trying to get new version:\n\n{e}\n")
            time.sleep(45)
            continue

        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)

        if data["client_version"] != cacheFile["client_version"]:
            for key, value in data.items():
                for cachedKey, cachedValue in cacheFile.items():
                    if key == cachedKey:
                        if value != cachedValue:
                            file_manager.updateJson(config.CACHE_FILE_PATH, value, key)
            sys.exit()

        time.sleep(45)

def online_players():
    while True:
        value = client.get_player_count(730)
        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)

        if value != cacheFile["online_players"]:
            file_manager.updateJson(config.CACHE_FILE_PATH, value, "online_players")

        time.sleep(45)


def send_alert(newVal, key):
    bot = telebot.TeleBot(config.BOT_TOKEN)

    if key == "public_build_id":
        text = notifications.publicBuild.format(newVal)
    elif key == "dpr_build_id":
        text = notifications.dprBuild.format(newVal)
    elif key == "dprp_build_id":
        text = notifications.dprpBuild.format(newVal)
    elif key == "dpr_build_sync_id":
        text = f"{notifications.dprBuild.format(newVal)} 🔃"
    elif key == "sdk_build_id":
        text = notifications.sdkBuild.format(newVal)
    elif key == "ds_build_id":
        text = notifications.dsBuild.format(newVal)
    elif key == "valve_ds_changenumber":
        text = notifications.valveDS.format(newVal)

    if not config.TEST_MODE:
        chat_list = [config.INCS2CHAT, config.CSTRACKER]
    else:
        chat_list = [config.AQ]

    for chatID in chat_list:
        msg = bot.send_message(
            chatID, text, parse_mode="html", disable_web_page_preview=True
        )
        if chatID == config.INCS2CHAT:
            bot.pin_chat_message(msg.chat.id, msg.id, disable_notification=True)


try:
    result = client.login(username=config.STEAM_USERNAME, password=config.STEAM_PASS)

    if result != EResult.OK:
        print(f"\n> Failed to login: {repr(result)}\n")
        raise SystemExit

    client.run_forever()

except KeyboardInterrupt:
    if client.connected:
        print("\n> Logout\n")
        client.logout()
