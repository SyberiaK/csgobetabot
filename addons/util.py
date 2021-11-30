import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


import time
from datetime import datetime


from addons import file_manager, strings
from addons.plugins import time_converter, translate
import config


def server_status():
    '''Get the status of CS:GO servers'''
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    gcCache = cacheFile['game_coordinator']
    slCache = cacheFile['sessionsLogon']
    sCache = cacheFile['scheduler']
    piCache = cacheFile['steam_community']
    wsCache = cacheFile['valve_webapi']

    array = [gcCache, slCache, sCache, piCache, wsCache]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    gcRCache, slRCache, sRCache, piRCache, wsRCache = array_ru[
        0], array_ru[1], array_ru[2], array_ru[3], array_ru[4]

    if gcCache != 'normal' or slCache != 'normal':
        tick = '❌'
    else:
        tick = '✅'

    status_text_en = strings.status_en.format(
        tick, gcCache, slCache, sCache, piCache, wsCache)
    status_text_ru = strings.status_ru.format(
        tick, gcRCache, slRCache, sRCache, piRCache, wsRCache)

    server_status_text_en = status_text_en + '\n\n' + strings.last_upd_en.format(tsCache)
    server_status_text_ru = status_text_ru + '\n\n' + strings.last_upd_ru.format(tsRCache)

    if ((datetime.today().weekday() == 1 and datetime.now().hour > 21) or (datetime.today().weekday() == 2 and datetime.now().hour < 4)) and (gcCache != 'normal' or slCache != 'normal'):
        server_status_text_en = server_status_text_en + '\n\n' + strings.maintenance_en
        server_status_text_ru = server_status_text_ru + '\n\n' + strings.maintenance_ru

    return server_status_text_en, server_status_text_ru


def mm_stats():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    gcCache = cacheFile['game_coordinator']
    slCache = cacheFile['sessionsLogon']
    url = cacheFile['graph_url']
    pcCache, scCache = cacheFile['online_player_count'], cacheFile['online_server_count']
    apCache, ssCache, spCache = cacheFile['active_player_count'], cacheFile['search_seconds_avg'], cacheFile['searching_players']
    p24Cache, paCache, uqCache = cacheFile['peak_24_hours'], cacheFile['peak_all_time'], cacheFile['unique_monthly']

    mm_text_en = strings.mm_en.format(
        url, scCache, pcCache, apCache, spCache, ssCache)
    mm_text_ru = strings.mm_ru.format(
        url, scCache, pcCache, apCache, spCache, ssCache)

    addInf_text_en = strings.additionalInfo_en.format(
        p24Cache, paCache, uqCache)
    addInf_text_ru = strings.additionalInfo_ru.format(
        p24Cache, paCache, uqCache)

    mm_stats_text_en = mm_text_en + '\n\n' + addInf_text_en + '\n\n' + strings.last_upd_en.format(tsCache)
    mm_stats_text_ru = mm_text_ru + '\n\n' + addInf_text_ru + '\n\n' + strings.last_upd_ru.format(tsRCache)

    if ((datetime.today().weekday() == 1 and datetime.now().hour > 21) or (datetime.today().weekday() == 2 and datetime.now().hour < 4)) and (gcCache != 'normal' or slCache != 'normal'):
        mm_stats_text_en = mm_stats_text_en + '\n\n' + strings.maintenance_en
        mm_stats_text_ru = mm_stats_text_ru + '\n\n' + strings.maintenance_ru

    return mm_stats_text_en, mm_stats_text_ru


def devcount():
    '''Get the count of online devs'''
    tsCache, tsRCache, tsVCache, tsVRCache = time_converter()[0], time_converter()[
        1], time_converter()[4], time_converter()[5]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    url = cacheFile['graph_url2']
    dcCache, dpCache = cacheFile['dev_player_count'], cacheFile['dev_all_time_peak']
    devcount_text_en = strings.devCount_en.format(
        url, dcCache, dpCache, tsCache, tsVCache)
    devcount_text_ru = strings.devCount_ru.format(
        url, dcCache, dpCache, tsRCache, tsVRCache)
    return devcount_text_en, devcount_text_ru


def timer():
    '''Get drop cap reset time'''
    wanted_day = 'wednesday'
    wanted_time = 00

    list = [['monday', 0], ['tuesday', 1], ['wednesday', 2], [
        'thursday', 3], ['friday', 4], ['saturday', 5], ['sunday', 6]]

    for i in list:
        if wanted_day == i[0]:
            number_wanted_day = i[1]

    today = datetime.today().weekday()
    
    delta_days = number_wanted_day - today
    actual_time = time.localtime(time.time())

    if wanted_time > actual_time[3]:
        delta_hours = wanted_time - actual_time[3]
        delta_mins = 59 - actual_time[4]
        delta_secs = 59 - actual_time[5]
    else:
        delta_days = delta_days - 1
        delta_hours = 23 - actual_time[3] + wanted_time
        delta_mins = 59 - actual_time[4]
        delta_secs = 59 - actual_time[5]

    if delta_days < 0:
        delta_days = delta_days + 7
    timer_text_en = strings.timer_en.format(
        delta_days, delta_hours, delta_mins, delta_secs)
    timer_text_ru = strings.timer_ru.format(
        delta_days, delta_hours, delta_mins, delta_secs)
    return timer_text_en, timer_text_ru


def gameversion():
    '''Get the version of the game'''
    vdCache, vdRCache = time_converter()[2], time_converter()[3]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    cvCache, svCache, pvCache = cacheFile['client_version'], cacheFile['server_version'], cacheFile['patch_version']
    gameversion_text_en = strings.gameversion_en.format(
        pvCache, cvCache, svCache, vdCache)
    gameversion_text_ru = strings.gameversion_ru.format(
        pvCache, cvCache, svCache, vdRCache)
    return gameversion_text_en, gameversion_text_ru


def gun_info(gun_id):
    '''Get archived data about guns'''
    cacheFile = file_manager.readJson(config.GUNS_CACHE_FILE_PATH)
    raw_data = list(filter(lambda x: x['id'] == gun_id, cacheFile['data']))
    data = raw_data[0]
    key_list = []
    value_list = []
    for key, value in data.items():
        key_list.append(key)
        value_list.append(value)
    name, price = value_list[1], value_list[2]
    origin, origin_ru = value_list[3], ''
    clip_size, reserve_ammo = value_list[4], value_list[5]
    fire_rate, kill_reward, movement_speed = value_list[6], value_list[10], value_list[8]
    armor_penetration, accurate_range_stand, accurate_range_crouch = value_list[
        9], value_list[11], value_list[12]
    draw_time, reload_clip_ready, reload_fire_ready = value_list[
        13], value_list[14], value_list[15]
    origin_list_ru = ['Германия', 'Австрия', 'Италия', 'Швейцария', 'Чехия', 'Бельгия', 'Швеция', 'Израль',
                      'Соединённые Штаты', 'Россия', 'Франция', 'Соединённое Королевство', 'Южная Африка']
    origin_list_en = ['Germany', 'Austria', 'Italy', 'Switzerland', 'Czech Republic', 'Belgium', 'Sweden', 'Israel',
                      'United States', 'Russia', 'France', 'United Kingdom', 'South Africa']
    unarmored_damage_head, unarmored_damage_chest_and_arm, unarmored_damage_stomach, unarmored_damage_leg = value_list[
        16], value_list[17], value_list[18], value_list[19]
    armored_damage_head, armored_damage_chest_and_arm, armored_damage_stomach, armored_damage_leg = value_list[
        20], value_list[21], value_list[22], value_list[23]
    for en, ru in zip(origin_list_en, origin_list_ru):
        if origin in en:
            origin_ru = ru
    gun_data_text_en = strings.gun_data_en.format(name, origin, price, clip_size, reserve_ammo, fire_rate, kill_reward, movement_speed,
                                                  armor_penetration, accurate_range_stand, accurate_range_crouch, draw_time, reload_clip_ready, reload_fire_ready,
                                                  armored_damage_head, unarmored_damage_head, armored_damage_chest_and_arm, unarmored_damage_chest_and_arm,
                                                  armored_damage_stomach, unarmored_damage_stomach, armored_damage_leg, unarmored_damage_leg)
    gun_data_text_ru = strings.gun_data_ru.format(name, origin_ru, price, clip_size, reserve_ammo, fire_rate, kill_reward, movement_speed,
                                                  armor_penetration, accurate_range_stand, accurate_range_crouch, draw_time, reload_clip_ready, reload_fire_ready,
                                                  armored_damage_head, unarmored_damage_head, armored_damage_chest_and_arm, unarmored_damage_chest_and_arm,
                                                  armored_damage_stomach, unarmored_damage_stomach, armored_damage_leg, unarmored_damage_leg)
    return gun_data_text_en, gun_data_text_ru