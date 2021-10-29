import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


from steam.client import SteamClient
from steam.enums import EResult
from csgo.client import CSGOClient
import logging


import config
import file_manager


logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s | %(name)s: %(message)s', datefmt='%H:%M:%S — %d/%m/%Y')


client = SteamClient()
cs = CSGOClient(client)
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
    cs.launch()


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


try:
    result = client.login(username=config.STEAM_USERNAME_ALT,
                          password=config.STEAM_PASS_ALT)

    if result != EResult.OK:
        print(f"\n> Failed to login: {repr(result)}\n")
        raise SystemExit

    client.run_forever()
except KeyboardInterrupt:
    if client.connected:
        print("\n> Logout\n")
        client.logout()
