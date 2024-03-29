from datetime import datetime, timedelta

import config
import pytz
import validators
from babel.dates import format_datetime

from addons import file_manager

tz = pytz.timezone("UTC")
tz_valve = pytz.timezone("America/Los_Angeles")


def time_converter():
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    if cacheFile["api_timestamp"] == 'unknown':
        steam_server_time = csgoVDCache = cs2VDCache = tsVCache = 'unknown'
        tsRCache = csgoVDRCache = cs2VDRCache = tsVRCache = 'неизвестно'
    else:
        steam_server_time = datetime.fromtimestamp(cacheFile["api_timestamp"], tz=tz).strftime("%H:%M:%S, %d %b %Z")
        temp1 = steam_server_time.rsplit(" ", 1)[0]
        tsRCache = f'{format_datetime(datetime.strptime(temp1, "%H:%M:%S, %d %b"), "HH:mm:ss, dd MMM", locale="ru",).title()} ({steam_server_time.split()[-1]})'

        csgo_version_date = cacheFile["csgo_version_timestamp"]
        csgoVDCache = (datetime.fromtimestamp(csgo_version_date, tz=tz) + timedelta(hours=8)).strftime("%H:%M:%S, %d %b %Z")
        temp2 = csgoVDCache.rsplit(" ", 1)[0]
        csgoVDRCache = f'{format_datetime(datetime.strptime(temp2, "%H:%M:%S, %d %b"), "HH:mm:ss, dd MMM", locale="ru",).title()} ({csgoVDCache.split()[-1]})'

        cs2_version_date = cacheFile["cs2_version_timestamp"]
        cs2VDCache = (datetime.fromtimestamp(cs2_version_date, tz=tz) + timedelta(hours=8)).strftime("%H:%M:%S, %d %b %Z")
        temp2 = cs2VDCache.rsplit(" ", 1)[0]
        cs2VDRCache = f'{format_datetime(datetime.strptime(temp2, "%H:%M:%S, %d %b"), "HH:mm:ss, dd MMM", locale="ru",).title()} ({cs2VDCache.split()[-1]})'

        tsVCache = datetime.now(tz=tz_valve).strftime("%H:%M:%S, %d %b %Z")
        temp3 = tsVCache.rsplit(" ", 1)[0]
        tsVRCache = f'{format_datetime(datetime.strptime(temp3, "%H:%M:%S, %d %b"), "HH:mm:ss, dd MMM", locale="ru",).title()} ({tsVCache.split()[-1]})'

    return steam_server_time, tsRCache, csgoVDCache, csgoVDRCache, tsVCache, tsVRCache, cs2VDCache, cs2VDRCache


def translate(data):
    en_list = [
        "low",
        "medium",
        "high",
        "full",
        "normal",
        "surge",
        "delayed",
        "idle",
        "offline",
        "critical",
        "internal server error",
        "internal bot error",
        "reloading",
        "internal Steam error",
        "unknown",
    ]
    ru_list = [
        "низкая",
        "средняя",
        "высокая",
        "полная",
        "в норме",
        "помехи",
        "задержка",
        "бездействие",
        "офлайн",
        "критическое",
        "внутренняя ошибка сервера",
        "внутренняя ошибка бота",
        "перезагрузка",
        "внутренняя ошибка Steam",
        "неизвестно",
    ]
    for en, ru in zip(en_list, ru_list):
        if data in en:
            data_ru = ru
            return data_ru


def url_checker(data):
    if data.startswith("steamcommunity"):
        data = f"https://{data}"
    elif validators.url(data):
        pass
    elif data.isdigit() and str(data).startswith("7656") and len(data) == 17:
        data = f"https://steamcommunity.com/profiles/{data}"
    else:
        data = f"https://steamcommunity.com/id/{data}"
    return data
