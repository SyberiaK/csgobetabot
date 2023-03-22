import config
import requests

API_server_status = f"https://api.steampowered.com/ICSGOServers_730/GetGameServersStatus/v1?key={config.STEAM_API_KEY}"


class ValveServersAPI:
    def get_status(self):
        status = {
            "webapi": "unknown",
            "api_timestamp": "unknown",
            "sessions_logon": "unknown",
            "steam_community": "unknown",
            "matchmaking_scheduler": "unknown",
            "online_servers": "unknown",
            "active_players": "unknown",
            "searching_players": "unknown",
            "search_seconds_avg": "unknown",
            "datacenters": "unknown",
        }

        try:
            response = requests.get(API_server_status, timeout=15)
            if response.status_code == 200:
                webapi_status = "normal"
            else:
                webapi_status = "unknown"
            result = response.json()["result"]

            status["webapi"] = webapi_status
            status["api_timestamp"] = result["app"]["timestamp"]
            status["sessions_logon"] = result["services"]["SessionsLogon"]
            status["steam_community"] = result["services"]["SteamCommunity"]
            status["matchmaking_scheduler"] = result["matchmaking"]["scheduler"]
            status["online_servers"] = result["matchmaking"]["online_servers"]
            status["active_players"] = result["matchmaking"]["online_players"]
            status["searching_players"] = result["matchmaking"]["searching_players"]
            status["search_seconds_avg"] = result["matchmaking"]["search_seconds_avg"]
            status["datacenters"] = result["datacenters"]

            return status
        except:
            return status
