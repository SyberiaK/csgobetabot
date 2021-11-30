import config
from addons import file_manager, strings
from addons.plugins import translate, time_converter


def africa():
    try:
        tsCache, tsRCache = time_converter()[0], time_converter()[1]
        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        africa_dc = cacheFile['datacenters']['South Africa']
        capacity, load = africa_dc['capacity'], africa_dc['load']
    except:
        capacity = load = 'unknown'
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1]
    africa_text_ru = strings.dc_africa_ru.format(load_ru, capacity_ru) +'\n\n' + strings.last_upd_ru.format(tsRCache)
    africa_text_en = strings.dc_africa_en.format(load, capacity) + '\n\n' + strings.last_upd_en.format(tsCache)
    return africa_text_en, africa_text_ru


def australia():
    try:
        tsCache, tsRCache = time_converter()[0], time_converter()[1]
        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        australia_dc = cacheFile['datacenters']['Australia']
        capacity, load = australia_dc['capacity'], australia_dc['load']
    except:
        capacity = load = 'unknown'
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1]
    australia_text_ru = strings.dc_australia_ru.format(load_ru, capacity_ru) +'\n\n' + strings.last_upd_ru.format(tsRCache)
    australia_text_en = strings.dc_australia_en.format(load, capacity) + '\n\n' + strings.last_upd_en.format(tsCache)
    return australia_text_en, australia_text_ru


def eu_north():
    try:
        tsCache, tsRCache = time_converter()[0], time_converter()[1]
        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        sweden_dc = cacheFile['datacenters']['EU North']
        capacity, load = sweden_dc['capacity'], sweden_dc['load']
    except:
        capacity = load = 'unknown'
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1]
    eu_north_text_ru = strings.dc_north_eu_ru.format(load_ru, capacity_ru) +'\n\n' + strings.last_upd_ru.format(tsRCache)
    eu_north_text_en = strings.dc_north_eu_en.format(load, capacity) + '\n\n' + strings.last_upd_en.format(tsCache)
    return eu_north_text_en, eu_north_text_ru


def eu_west():
    try:
        tsCache, tsRCache = time_converter()[0], time_converter()[1]
        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        germany_dc = cacheFile['datacenters']['EU West']
        spain_dc = cacheFile['datacenters']['Spain']
        capacity, load = germany_dc['capacity'], germany_dc['load']
        capacity_secondary, load_secondary = spain_dc['capacity'], spain_dc['load']
    except:
        capacity = load = capacity_secondary = load_secondary = 'unknown'
    array = [capacity, load, capacity_secondary, load_secondary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru = array_ru[
        0], array_ru[1], array_ru[2], array_ru[3]
    eu_west_text_ru = strings.dc_west_eu_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru) +'\n\n' + strings.last_upd_ru.format(tsRCache)
    eu_west_text_en = strings.dc_west_eu_en.format(load, capacity, load_secondary, capacity_secondary) + '\n\n' + strings.last_upd_en.format(tsCache)
    return eu_west_text_en, eu_west_text_ru


def eu_east():
    try:
        tsCache, tsRCache = time_converter()[0], time_converter()[1]
        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        austria_dc = cacheFile['datacenters']['EU East']
        poland_dc = cacheFile['datacenters']['Poland']
        capacity, load = austria_dc['capacity'], austria_dc['load']
        capacity_secondary, load_secondary = poland_dc['capacity'], poland_dc['load']
    except:
        capacity = load = capacity_secondary = load_secondary = 'unknown'
    array = [capacity, load, capacity_secondary, load_secondary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru = array_ru[
        0], array_ru[1], array_ru[2], array_ru[3]
    eu_east_text_ru = strings.dc_east_eu_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru) +'\n\n' + strings.last_upd_ru.format(tsRCache)
    eu_east_text_en = strings.dc_east_eu_en.format(load, capacity, load_secondary, capacity_secondary) + '\n\n' + strings.last_upd_en.format(tsCache)
    return eu_east_text_en, eu_east_text_ru


def usa_north():
    try:
        tsCache, tsRCache = time_converter()[0], time_converter()[1]
        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        chicago_dc = cacheFile['datacenters']['US Northcentral']
        sterling_dc = cacheFile['datacenters']['US Northeast']
        moseslake_dc = cacheFile['datacenters']['US Northwest']
        capacity, load = chicago_dc['capacity'], chicago_dc['load']
        capacity_secondary, load_secondary = sterling_dc['capacity'], sterling_dc['load']
        capacity_tertiary, load_tertiary = moseslake_dc['capacity'], moseslake_dc['load']
    except:
        capacity = load = capacity_secondary = load_secondary = capacity_tertiary = load_tertiary = 'unknown'
    array = [capacity, load, capacity_secondary,
             load_secondary, capacity_tertiary, load_tertiary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru, capacity_tertiary_ru, load_tertiary_ru = array_ru[
        0], array_ru[1], array_ru[2], array_ru[3], array_ru[4], array_ru[5]
    usa_north_text_ru = strings.dc_north_us_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, load_tertiary_ru, capacity_tertiary_ru) +'\n\n' + strings.last_upd_ru.format(tsRCache)
    usa_north_text_en = strings.dc_north_us_en.format(load, capacity, load_secondary, capacity_secondary, load_tertiary, capacity_tertiary) + '\n\n' + strings.last_upd_en.format(tsCache)
    return usa_north_text_en, usa_north_text_ru


def usa_south():
    try:
        tsCache, tsRCache = time_converter()[0], time_converter()[1]
        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        losangeles_dc = cacheFile['datacenters']['US Southwest']
        atlanta_dc = cacheFile['datacenters']['US Southeast']
        capacity, load = losangeles_dc['capacity'], losangeles_dc['load']
        capacity_secondary, load_secondary = atlanta_dc['capacity'], atlanta_dc['load']
    except:
        capacity = load = capacity_secondary = load_secondary = 'unknown'
    array = [capacity, load, capacity_secondary, load_secondary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru = array_ru[
        0], array_ru[1], array_ru[2], array_ru[3]
    usa_south_text_ru = strings.dc_south_us_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru) +'\n\n' + strings.last_upd_ru.format(tsRCache)
    usa_south_text_en = strings.dc_south_us_en.format(load, capacity, load_secondary, capacity_secondary) + '\n\n' + strings.last_upd_en.format(tsCache)
    return usa_south_text_en, usa_south_text_ru


def south_america():
    try:
        tsCache, tsRCache = time_converter()[0], time_converter()[1]
        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        brazil_dc = cacheFile['datacenters']['Brazil']
        chile_dc = cacheFile['datacenters']['Chile']
        peru_dc = cacheFile['datacenters']['Peru']
        argentina_dc = cacheFile['datacenters']['Argentina']
        capacity, load = brazil_dc['capacity'], brazil_dc['load']
        capacity_secondary, load_secondary = chile_dc['capacity'], chile_dc['load']
        capacity_tertiary, load_tertiary = peru_dc['capacity'], peru_dc['load']
        capacity_quaternary, load_quaternary = argentina_dc['capacity'], argentina_dc['load']
    except:
        capacity = load = capacity_secondary = load_secondary = capacity_tertiary = load_tertiary = capacity_quaternary = load_quaternary = 'unknown'
    array = [capacity, load, capacity_secondary, load_secondary,
             capacity_tertiary, load_tertiary, capacity_quaternary, load_quaternary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary_ru, load_quaternary_ru = array_ru[
        0], array_ru[1], array_ru[2], array_ru[3], array_ru[4], array_ru[5], array_ru[6], array_ru[7]
    south_america_text_ru = strings.dc_south_america_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, load_tertiary_ru, capacity_tertiary_ru, load_quaternary_ru, capacity_quaternary_ru) +'\n\n' + strings.last_upd_ru.format(tsRCache)
    south_america_text_en = strings.dc_south_america_en.format(load, capacity, load_secondary, capacity_secondary, load_tertiary, capacity_tertiary, load_quaternary, capacity_quaternary) + '\n\n' + strings.last_upd_en.format(tsCache)
    return south_america_text_en, south_america_text_ru


def india():
    try:
        tsCache, tsRCache = time_converter()[0], time_converter()[1]
        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        mumbai_dc = cacheFile['datacenters']['India']
        chennai_dc = cacheFile['datacenters']['India East']
        capacity, load = mumbai_dc['capacity'], mumbai_dc['load']
        capacity_secondary, load_secondary = chennai_dc['capacity'], chennai_dc['load']
    except:
        capacity = load = capacity_secondary = load_secondary = 'unknown'
    array = [capacity, load, capacity_secondary, load_secondary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru = array_ru[
        0], array_ru[1], array_ru[2], array_ru[3]
    india_text_ru = strings.dc_india_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru) +'\n\n' + strings.last_upd_ru.format(tsRCache)
    india_text_en = strings.dc_india_en.format(load, capacity, load_secondary, capacity_secondary) + '\n\n' + strings.last_upd_en.format(tsCache)
    return india_text_en, india_text_ru


def japan():
    try:
        tsCache, tsRCache = time_converter()[0], time_converter()[1]
        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        japan_dc = cacheFile['datacenters']['Japan']
        capacity, load = japan_dc['capacity'], japan_dc['load']
    except:
        capacity = load = 'unknown'    
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1]
    japan_text_ru = strings.dc_japan_ru.format(load_ru, capacity_ru) +'\n\n' + strings.last_upd_ru.format(tsRCache)
    japan_text_en = strings.dc_japan_en.format(load, capacity) + '\n\n' + strings.last_upd_en.format(tsCache)
    return japan_text_en, japan_text_ru


def china():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    shanghai_dc = cacheFile['datacenters']['China Shanghai']
    tianjin_dc = cacheFile['datacenters']['China Tianjin']
    guangzhou_dc = cacheFile['datacenters']['China Guangzhou']
    capacity, load = shanghai_dc['capacity'], shanghai_dc['load']
    capacity_secondary, load_secondary = tianjin_dc['capacity'], tianjin_dc['load']
    capacity_tertiary, load_tertiary = guangzhou_dc['capacity'], guangzhou_dc['load']
    array = [capacity, load, capacity_secondary,
             load_secondary, capacity_tertiary, load_tertiary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru, capacity_tertiary_ru, load_tertiary_ru = array_ru[
        0], array_ru[1], array_ru[2], array_ru[3], array_ru[4], array_ru[5]
    china_text_ru = strings.dc_china_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, load_tertiary_ru, capacity_tertiary_ru) +'\n\n' + strings.last_upd_ru.format(tsRCache)
    china_text_en = strings.dc_china_en.format(load, capacity, load_secondary, capacity_secondary, load_tertiary, capacity_tertiary) + '\n\n' + strings.last_upd_en.format(tsCache)
    return china_text_en, china_text_ru


def emirates():
    try:
        tsCache, tsRCache = time_converter()[0], time_converter()[1]
        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        emirates_dc = cacheFile['datacenters']['Emirates']
        capacity, load = emirates_dc['capacity'], emirates_dc['load']
    except:
        capacity = load = 'unknown'
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1]
    emirates_text_ru = strings.dc_emirates_ru.format(load_ru, capacity_ru) +'\n\n' + strings.last_upd_ru.format(tsRCache)
    emirates_text_en = strings.dc_emirates_en.format(load, capacity) + '\n\n' + strings.last_upd_en.format(tsCache)
    return emirates_text_en, emirates_text_ru


def singapore():
    try:
        tsCache, tsRCache = time_converter()[0], time_converter()[1]
        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        singapore_dc = cacheFile['datacenters']['Singapore']
        capacity, load = singapore_dc['capacity'], singapore_dc['load']
    except:
        capacity = load = 'unknown'
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1]
    singapore_text_ru = strings.dc_singapore_ru.format(load_ru, capacity_ru) +'\n\n' + strings.last_upd_ru.format(tsRCache)
    singapore_text_en = strings.dc_singapore_en.format(load, capacity) + '\n\n' + strings.last_upd_en.format(tsCache)
    return singapore_text_en, singapore_text_ru


def hong_kong():
    try:
        tsCache, tsRCache = time_converter()[0], time_converter()[1]
        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        hongkong_dc = cacheFile['datacenters']['Hong Kong']
        capacity, load = hongkong_dc['capacity'], hongkong_dc['load']
    except:
        capacity = load = 'unknown'
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1]
    hong_kong_text_ru = strings.dc_hong_kong_ru.format(load_ru, capacity_ru) +'\n\n' + strings.last_upd_ru.format(tsRCache)
    hong_kong_text_en = strings.dc_hong_kong_en.format(load, capacity) + '\n\n' + strings.last_upd_en.format(tsCache)
    return hong_kong_text_en, hong_kong_text_ru


def south_korea():
    try:
        tsCache, tsRCache = time_converter()[0], time_converter()[1]
        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        south_korea_dc = cacheFile['datacenters']['South Korea']
        capacity, load = south_korea_dc['capacity'], south_korea_dc['load']
    except:
        capacity = load = 'unknown'
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1]
    south_korea_text_ru = strings.dc_south_korea_ru.format(load_ru, capacity_ru) +'\n\n' + strings.last_upd_ru.format(tsRCache)
    south_korea_text_en = strings.dc_south_korea_en.format(load, capacity) + '\n\n' + strings.last_upd_en.format(tsCache)
    return south_korea_text_en, south_korea_text_ru
