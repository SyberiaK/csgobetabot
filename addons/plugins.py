from datetime import datetime, timedelta
import pytz
from babel.dates import format_datetime
import validators


from addons import file_manager
import config


tz = pytz.timezone('UTC')
tz_valve = pytz.timezone('America/Los_Angeles')


def time_converter():
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    time_server = cacheFile['server_timestamp']
    tsCache = datetime.fromtimestamp(
        time_server, tz=tz).strftime('%H:%M:%S — %d %b %Y %Z')
    temp1 = tsCache.rsplit(' ', 1)[0]
    tsRCache = str(format_datetime(datetime.strptime(
        temp1, '%H:%M:%S — %d %b %Y'), 'HH:mm:ss — dd MMM yyyy', locale='ru')).title() + ' ' + str(tsCache.split()[-1])

    version_date = cacheFile['version_timestamp']
    vdCache = (datetime.fromtimestamp(version_date, tz=tz) +
               timedelta(hours=8)).strftime('%H:%M:%S — %d %b %Y %Z')
    temp2 = vdCache.rsplit(' ', 1)[0]
    vdRCache = str(format_datetime(datetime.strptime(
        temp2, '%H:%M:%S — %d %b %Y'), 'HH:mm:ss — dd MMM yyyy', locale='ru')).title() + ' ' + str(tsCache.split()[-1])

    tsVCache = datetime.now(tz=tz_valve).strftime('%H:%M:%S — %d %b %Y %Z')
    temp3 = tsVCache.rsplit(' ', 1)[0]
    tsVRCache = str(format_datetime(datetime.strptime(
        temp3, '%H:%M:%S — %d %b %Y'), 'HH:mm:ss — dd MMM yyyy', locale='ru')).title() + ' ' + str(tsVCache.split()[-1])

    return tsCache, tsRCache, vdCache, vdRCache, tsVCache, tsVRCache


def translate(data):
    en_list = ['low', 'medium', 'high', 'full', 'normal', 'surge', 'delayed',
               'idle', 'offline', 'critical', 'internal server error',
               'internal bot error', 'reloading', 'internal Steam error', 'unknown']
    ru_list = ['низкая', 'средняя', 'высокая', 'полная', 'в норме', 'помехи', 'задержка',
               'бездействие', 'офлайн', 'критическое', 'внутренняя ошибка сервера',
               'внутренняя ошибка бота', 'перезагрузка', 'внутренняя ошибка Steam', 'неизвестно']
    for en, ru in zip(en_list, ru_list):
        if data in en:
            data_ru = ru
            return data_ru


def url_checker(data):
    if data.startswith('steamcommunity'):
        data = 'https://' + data
    elif validators.url(data):
        pass
    elif data.isdigit() and len(data) == 17:
        data = f'https://steamcommunity.com/profiles/{data}'
    else:
        data = f'https://steamcommunity.com/id/{data}'
    return data
