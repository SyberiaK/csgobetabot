import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


from steam.client import SteamClient
from csgo.client import CSGOClient
import logging


import config
import file_manager


def coordinator_status():
    client = SteamClient()
    cs = CSGOClient(client)

    @client.on('logged_on')
    def start_csgo():
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
 
    client.login(username=config.STEAM_USERNAME_ALT,
                 password=config.STEAM_PASS_ALT)
    client.run_forever()

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s %(name)s: %(message)s', datefmt='%H:%M:%S — %d/%m/%Y')
    coordinator_status()