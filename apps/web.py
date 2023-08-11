import re
from datetime import datetime

import config
import requests
from bs4 import BeautifulSoup

monthly_api = "https://api.steampowered.com/ICSGOServers_730/GetMonthlyPlayerCount/v1"
csgo_url_github = "https://raw.githubusercontent.com/SteamDatabase/GameTracking-CSGO/master/csgo/steam.inf"
cs2_url_github = "https://raw.githubusercontent.com/SteamDatabase/GameTracking-CSGO/master/game/csgo/steam.inf"
asset_api = f"https://api.steampowered.com/ISteamEconomy/GetAssetPrices/v1/?appid={config.CSGO_APP_ID}&key={config.STEAM_API_KEY}"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0"
}


class Monthly:
    def get_unique(self):
        players = {"monthly_unique_players": "unknown"}
        try:
            response = requests.get(monthly_api, headers=headers, timeout=15).json()
            players["monthly_unique_players"] = int(response['result']['players'])
            return players
        except:
            return players


class GameVersion:
    def get_gameVer(self):
        dataset = {
            "csgo_client_version": "unknown",
            "csgo_server_version": "unknown",
            "csgo_patch_version": "unknown",
            "csgo_version_timestamp": "unknown",
            "cs2_client_version": "unknown",
            "cs2_server_version": "unknown",
            "cs2_patch_version": "unknown",
            "cs2_version_timestamp": "unknown",
        }
        try:
            soup = BeautifulSoup(
                requests.get(csgo_url_github, headers=headers, timeout=15).content,
                "html.parser",
            )

            data = soup.get_text()
            options = {}
            config_entries = re.split("\n|=", data)

            for key, value in zip(config_entries[0::2], config_entries[1::2]):
                cleaned_key = key.replace("[", "").replace("]", "")
                options[cleaned_key] = value

            dt = f'{options["VersionDate"]} {options["VersionTime"]}'

            dataset["csgo_client_version"] = int(options["ClientVersion"])
            dataset["csgo_server_version"] = int(options["ServerVersion"])
            dataset["csgo_patch_version"] = options["PatchVersion"]
            dataset["csgo_version_timestamp"] = datetime.strptime(
                dt, "%b %d %Y %H:%M:%S"
            ).timestamp()

            soup = BeautifulSoup(
                requests.get(cs2_url_github, headers=headers, timeout=15).content,
                "html.parser",
            )

            data = soup.get_text()
            options = {}
            config_entries = re.split("\n|=", data)

            for key, value in zip(config_entries[0::2], config_entries[1::2]):
                cleaned_key = key.replace("[", "").replace("]", "")
                options[cleaned_key] = value

            dt = f'{options["VersionDate"]} {options["VersionTime"]}'

            dataset["cs2_client_version"] = int(options["ClientVersion"]) - 2000000
            dataset["cs2_server_version"] = int(options["ServerVersion"]) - 2000000
            dataset["cs2_patch_version"] = options["PatchVersion"]
            dataset["cs2_version_timestamp"] = datetime.strptime(
                dt, "%b %d %Y %H:%M:%S"
            ).timestamp()


            return dataset
        except:
            return dataset


class Currency:
    def get_currency(self):
        try:
            r = requests.get(asset_api, timeout=15).json()["result"]["assets"]
            key_price = list(filter(lambda cur: cur["classid"] == "1544098059", r))
            del key_price[0]["prices"]["Unknown"]
            del key_price[0]["prices"]["BYN"]
            return key_price[0]["prices"]
        except Exception as e:
            return e
