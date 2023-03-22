import re
from datetime import datetime

import config
import requests
from bs4 import BeautifulSoup

monthly_api = "https://api.steampowered.com/ICSGOServers_730/GetMonthlyPlayerCount/v1"
url_github = "https://raw.githubusercontent.com/SteamDatabase/GameTracking-CSGO/master/csgo/steam.inf"
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
            "client_version": "unknown",
            "server_version": "unknown",
            "patch_version": "unknown",
            "version_timestamp": "unknown",
        }
        try:
            soup = BeautifulSoup(
                requests.get(url_github, headers=headers, timeout=15).content,
                "html.parser",
            )

            data = soup.get_text()
            options = {}
            config_entries = re.split("\n|=", data)

            for key, value in zip(config_entries[0::2], config_entries[1::2]):
                cleaned_key = key.replace("[", "").replace("]", "")
                options[cleaned_key] = value

            dt = f'{options["VersionDate"]} {options["VersionTime"]}'

            dataset["client_version"] = int(options["ClientVersion"])
            dataset["server_version"] = int(options["ServerVersion"])
            dataset["patch_version"] = options["PatchVersion"]
            dataset["version_timestamp"] = datetime.strptime(
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
