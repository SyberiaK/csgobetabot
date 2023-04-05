from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

# Delete keyboard
markup_del = ReplyKeyboardRemove(False)


### English ###


# Back button
back_button_en = KeyboardButton("⏪ Back")

# Channel link for inline messages
markup_inline_button_en = InlineKeyboardMarkup()
inline_button_channel_link_en = InlineKeyboardButton(
    "by Aquarius with ❤️", "https://twitter.com/aquaismissing"
)
markup_inline_button_en.add(inline_button_channel_link_en)

# Default
markup_en = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
server_stats_en = KeyboardButton("Server statistics")
profile_info_en = KeyboardButton("Profile information")
extra_features_en = KeyboardButton("Extra features")
markup_en.add(server_stats_en, profile_info_en, extra_features_en)

# Server Statistics
markup_ss_en = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
server_status_en = KeyboardButton("Service status")
matchmaking_en = KeyboardButton("Matchmaking status")
dc_en = KeyboardButton("Dataсenters status")
markup_ss_en.add(server_status_en, matchmaking_en, dc_en, back_button_en)

# Profile Information
markup_profile_en = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
profile_info_en = KeyboardButton("Bans and restrictions")
csgo_stats_en = KeyboardButton("CS in-game statistics")
markup_profile_en.add(profile_info_en, csgo_stats_en, back_button_en)

# Extra Features
markup_extra_en = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
crosshair_en = KeyboardButton("🆕 Crosshair")
currency_en = KeyboardButton("🆕 CS exchange rate")
valvetime_en = KeyboardButton("Time in Valve HQ")
timer_en = KeyboardButton("Cap reset")
gv_en = KeyboardButton("Game version")
guns_en = KeyboardButton("Gun database")
markup_extra_en.add(
    crosshair_en, currency_en, valvetime_en, gv_en, timer_en, guns_en, back_button_en
)

# DC
markup_DC_en = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
europe_en = KeyboardButton("Europe")
asia_en = KeyboardButton("Asia")
south_africa_en = KeyboardButton("South Africa")
south_america_en = KeyboardButton("South America")
australia_en = KeyboardButton("Australia")
usa_en = KeyboardButton("USA")
markup_DC_en.add(
    asia_en,
    australia_en,
    europe_en,
    south_africa_en,
    south_america_en,
    usa_en,
    back_button_en,
)

# DC Asia
markup_DC_Asia_en = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
india_en = KeyboardButton("India")
emirates_en = KeyboardButton("Emirates")
china_en = KeyboardButton("China")
singapore_en = KeyboardButton("Singapore")
hong_kong_en = KeyboardButton("Hong Kong")
japan_en = KeyboardButton("Japan")
south_korea_en = KeyboardButton("South Korea")
markup_DC_Asia_en.add(
    china_en,
    emirates_en,
    hong_kong_en,
    south_korea_en,
    india_en,
    japan_en,
    singapore_en,
)
markup_DC_Asia_en.add(back_button_en)

# DC Europe
markup_DC_EU_en = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
eu_West_en = KeyboardButton("West")
eu_East_en = KeyboardButton("East")
eu_North_en = KeyboardButton("North")
markup_DC_EU_en.add(eu_East_en, eu_North_en, eu_West_en, back_button_en)

# DC USA
markup_DC_USA_en = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
usa_Northwest_en = KeyboardButton("North")
usa_Southwest_en = KeyboardButton("South")
markup_DC_USA_en.add(usa_Northwest_en, usa_Southwest_en, back_button_en)

# Guns
markup_guns_en = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
pistols_en = KeyboardButton("Pistols")
smgs_en = KeyboardButton("SMGs")
rifles_en = KeyboardButton("Rifles")
heavy_en = KeyboardButton("Heavy")
markup_guns_en.add(pistols_en, smgs_en, rifles_en, heavy_en, back_button_en)

# Pistols
markup_pistols_en = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
usps = KeyboardButton("USP-S")
p2000 = KeyboardButton("P2000")
glock = KeyboardButton("Glock-18")
dualies = KeyboardButton("Dual Berettas")
p250 = KeyboardButton("P250")
cz75 = KeyboardButton("CZ75-Auto")
five_seven = KeyboardButton("Five-SeveN")
tec = KeyboardButton("Tec-9")
deagle = KeyboardButton("Desert Eagle")
r8 = KeyboardButton("R8 Revolver")
markup_pistols_en.add(usps, p2000, glock, p250)
markup_pistols_en.add(dualies, cz75, five_seven)
markup_pistols_en.add(tec, deagle, r8)
markup_pistols_en.add(back_button_en)

# SMGs
markup_smgs_en = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
mp9 = KeyboardButton("MP9")
mac10 = KeyboardButton("MAC-10")
mp7 = KeyboardButton("MP7")
mp5 = KeyboardButton("MP5-SD")
ump = KeyboardButton("UMP-45")
p90 = KeyboardButton("P90")
pp = KeyboardButton("PP-Bizon")
markup_smgs_en.add(mp9, mac10, mp7, mp5, ump, p90, pp)
markup_smgs_en.add(back_button_en)

# Rifles
markup_rifles_en = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
famas = KeyboardButton("Famas")
galil = KeyboardButton("Galil AR")
m4a4 = KeyboardButton("M4A4")
m4a1 = KeyboardButton("M4A1-S")
ak = KeyboardButton("AK-47")
aug = KeyboardButton("AUG")
sg = KeyboardButton("SG 553")
ssg = KeyboardButton("SSG 08")
awp = KeyboardButton("AWP")
scar = KeyboardButton("SCAR-20")
g3sg1 = KeyboardButton("G3SG1")
markup_rifles_en.add(famas, galil, m4a4, m4a1, ak, aug, sg, ssg, awp, scar, g3sg1)
markup_rifles_en.add(back_button_en)

# Heavy
markup_heavy_en = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
nova = KeyboardButton("Nova")
xm1014 = KeyboardButton("XM1014")
mag7 = KeyboardButton("MAG-7")
sawedoff = KeyboardButton("Sawed-Off")
m249 = KeyboardButton("M249")
negev = KeyboardButton("Negev")
markup_heavy_en.add(nova, xm1014, mag7, sawedoff, m249, negev, back_button_en)

# Crosshair
markup_crosshair_en = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
encode_en = KeyboardButton("Generate")
decode_en = KeyboardButton("Decode")
markup_crosshair_en.add(encode_en, decode_en, back_button_en)


### Russian ###


# Back button
back_button_ru = KeyboardButton("⏪ Назад")

# Channel link for inline messages
markup_inline_button_ru = InlineKeyboardMarkup()
inline_button_channel_link_ru = InlineKeyboardButton(
    "🔫 Обновления Counter-Strike", "https://t.me/INCS2"
)
markup_inline_button_ru.add(inline_button_channel_link_ru)

# Default
markup_ru = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
server_stats_ru = KeyboardButton("Статистика серверов")
profile_info_ru = KeyboardButton("Информация о профиле")
extra_features_ru = KeyboardButton("Дополнительные функции")
markup_ru.add(server_stats_ru, profile_info_ru, extra_features_ru)

# Server Statistics RU
markup_ss_ru = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
server_status_ru = KeyboardButton("Состояние служб")
mathcmaking_ru = KeyboardButton("Состояние матчмейкинга")
dc_ru = KeyboardButton("Состояние дата-центров")
markup_ss_ru.add(server_status_ru, mathcmaking_ru, dc_ru, back_button_ru)

# Profile information RU
markup_profile_ru = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
profile_info_ru = KeyboardButton("Запреты и ограничения")
csgo_stats_ru = KeyboardButton("Игровая статистика CS")
markup_profile_ru.add(profile_info_ru, csgo_stats_ru, back_button_ru)

# Extra Features RU
markup_extra_ru = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
crosshair_ru = KeyboardButton("🆕 Прицел")
currency_ru = KeyboardButton("🆕 Курс CS")
valvetime_ru = KeyboardButton("Время в штаб-кв. Valve")
gv_ru = KeyboardButton("Версия игры")
guns_ru = KeyboardButton("База данных оружий")
timer_ru = KeyboardButton("Сброс ограничений")
markup_extra_ru.add(
    crosshair_ru, currency_ru, valvetime_ru, gv_ru, timer_ru, guns_ru, back_button_ru
)

# DC
markup_DC_ru = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
europe_ru = KeyboardButton("Европа")
asia_ru = KeyboardButton("Азия")
africa_ru = KeyboardButton("Южная Африка")
south_america_ru = KeyboardButton("Южная Америка")
australia_ru = KeyboardButton("Австралия")
usa_ru = KeyboardButton("США")
markup_DC_ru.add(
    australia_ru,
    asia_ru,
    europe_ru,
    usa_ru,
    south_america_ru,
    africa_ru,
    back_button_ru,
)

# DC Europe
markup_DC_EU_ru = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
eu_West_ru = KeyboardButton("Запад")
eu_East_ru = KeyboardButton("Восток")
eu_North_ru = KeyboardButton("Север")
markup_DC_EU_ru.add(eu_East_ru, eu_West_ru, eu_North_ru, back_button_ru)

# DC Asia
markup_DC_Asia_ru = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
india_ru = KeyboardButton("Индия")
emirates_ru = KeyboardButton("Эмираты")
china_ru = KeyboardButton("Китай")
singapore_ru = KeyboardButton("Сингапур")
hong_kong_ru = KeyboardButton("Гонконг")
japan_ru = KeyboardButton("Япония")
south_korea_ru = KeyboardButton("Южная Корея")
markup_DC_Asia_ru.add(
    hong_kong_ru,
    india_ru,
    china_ru,
    south_korea_ru,
    singapore_ru,
    emirates_ru,
    japan_ru,
)
markup_DC_Asia_ru.add(back_button_ru)

# DC USA
markup_DC_USA_ru = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
usa_Northwest_ru = KeyboardButton("Север")
usa_Southwest_ru = KeyboardButton("Юг")
markup_DC_USA_ru.add(usa_Northwest_ru, usa_Southwest_ru, back_button_ru)

# Guns
markup_guns_ru = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
pistols = KeyboardButton("Пистолеты")
smgs = KeyboardButton("Пистолеты-пулемёты")
rifles = KeyboardButton("Винтовки")
heavy = KeyboardButton("Тяжёлое оружие")
markup_guns_ru.add(pistols, smgs, rifles, heavy, back_button_ru)

# Pistols
markup_pistols_ru = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
markup_pistols_ru.add(usps, p2000, glock, p250)
markup_pistols_ru.add(dualies, cz75, five_seven)
markup_pistols_ru.add(tec, deagle, r8)
markup_pistols_ru.add(back_button_ru)

# SMGs
markup_smgs_ru = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
markup_smgs_ru.add(mp9, mac10, mp7, mp5, ump, p90, pp)
markup_smgs_ru.add(back_button_ru)

# Rifles
markup_rifles_ru = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
markup_rifles_ru.add(famas, galil, m4a4, m4a1, ak, aug, sg, ssg, awp, scar, g3sg1)
markup_rifles_ru.add(back_button_ru)

# Heavy Russian
markup_heavy_ru = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
markup_heavy_ru.add(nova, xm1014, mag7, sawedoff, m249, negev, back_button_ru)

# Crosshair
markup_crosshair_ru = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
encode_ru = KeyboardButton("Создать")
decode_ru = KeyboardButton("Расшифровать")
markup_crosshair_ru.add(encode_ru, decode_ru, back_button_ru)
