### Text for default Commands
# English

cmdStart_en = """👋🏼 Hey, {}!
This bot is designed to check the number of online players and the availability of Counter-Strike servers.

For more information type /help."""
cmdHelp_en = """<a href="https://telegra.ph/Detailed-description-03-07">‎</a>ℹ️ This bot is developed by @INCS2. You can see the source code on <a href="https://github.com/csgobeta/csgobetabot">GitHub</a>.

telegra.ph/Detailed-description-03-07"""
cmdFeedback_en = """💬 Please, tell us about your <b>suggestions</b> or <b>problems</b> that you have encountered using our bot.

Use /cancel to cancel this command."""

# Russian
cmdStart_ru = """👋🏼 Привет, {}!
Этот бот предназначен для проверки количества онлайн игроков и доступности серверов Counter-Strike.

Для большей информации воспользуйтесь /help."""
cmdHelp_ru = """<a href="https://telegra.ph/Podrobnoe-opisanie-03-07">‎</a>ℹ️ Этот бот разработан каналом @INCS2. Исходный код можно найти на <a href="https://github.com/csgobeta/csgobetabot">GitHub</a>.

telegra.ph/Podrobnoe-opisanie-03-07"""
cmdFeedback_ru = """💬 Пожалуйста, расскажите о Ваших <b>пожеланиях</b> или <b>проблемах</b>, с которыми Вы столкнулись, используя бота.

Используйте /cancel, чтобы отменить команду."""


### Text for Last Updated
# English
last_upd_en = """Last data update: {}"""

# Russian
last_upd_ru = """Последнее обновление данных: {}"""


### Text for Counter-Strike Status
# English
status_en = """{} <b>Counter-Strike service status:</b>

• Game coordinator: {}
• Server connection: {}
• Matchmaking scheduler: {}
• Player inventories: {}
• Steam web API: {}"""

# Russian
status_ru = """{} <b>Состояние служб Counter-Strike:</b>

• Игровой координатор: {}
• Подключение к серверам: {}
• Планировщик матчмейкинга: {}
• Инвентари игроков: {}
• Steam веб-API: {}"""


### Text for Matchmaking Stats
# English
mm_en = """<a href="{}">‎</a>📊 <b>Matchmaking statistics:</b>

• Servers online: {:,}
• Players online: {:,}
• Players active: {:,}
• Players searching: {:,}
• Estimated search time: {}s"""

# Russian
mm_ru = """<a href="{}">‎</a>⁠📊 <b>Статистика матчмейкинга:</b>

• Серверов в сети: {:,}
• Игроков в сети: {:,}
• Активных игроков: {:,}
• Игроков в поиске: {:,}
• Примерное время поиска: {} с."""


### Text for Additional MM Stats
# English
additionalInfo_en = """📁 <b>Additional information:</b>

• 24-hour peak: {:,}
• All-time peak: {:,}
• Monthly unique players: {:,}"""

# Russian
additionalInfo_ru = """📁 <b>Дополнительная информация:</b>

• 24-часовой пик: {:,}
• Рекордный пик: {:,}
• Ежемесячные уникальные игроки: {:,}"""


### Text for Bellevue Time
# English
valve_time_en = """⏳ Time in Bellevue (Valve HQ): {}"""

# Russian
valve_time_ru = """⏳ Время в Белвью (штаб-кв. Valve): {}"""


### Text for Cap Timer
# English
timer_en = "⏳ Time left until experience and drop cap reset: {}d {}h {}m {}s"

# Russian
timer_ru = "⏳ Время до сброса ограничений опыта и дропа: {} д. {} ч. {} м. {} с."


### Text for Game Version
# English
gameversion_en = """⚙️ Current game version:

CS:GO: <code>{}</code> <code>({})</code>
Latest update: {}

CS2: <code>{}</code> <code>({})</code>
Latest update: {}"""

# Russian
gameversion_ru = """⚙️ Текущая версия игры:

CS:GO: <code>{}</code> <code>({})</code>
Последнее обновление: {}

CS2: <code>{}</code> <code>({})</code>
Последнее обновление: {}

ℹ️ Трекер обновлений Counter-Strike: <a href="http://t.me/cstracker/7">@cstracker</a>"""


### URL examples
# English
url_ex_en = """🔗 Please, enter one of the following options:
        
• Profile link (ex: <code>https://steamcommunity.com/id/aquaismissing</code>)
• Profile permalink (ex: <code>https://steamcommunity.com/profiles/76561198346163255</code>)
• SteamID (ex: <code>76561198346163255</code>)
• Custom URL (ex: <code>aquaismissing</code>)

Use /cancel to cancel this command."""

# Russian
url_ex_ru = """🔗 Пожалуйста, введите один из следующих вариантов:

• Ссылка на профиль (напр.: <code>https://steamcommunity.com/id/aquaismissing</code>)
• Перманентная ссылка на профиль (напр.: <code>https://steamcommunity.com/profiles/76561198346163255</code>)
• SteamID (напр.: <code>76561198346163255</code>)
• Личная ссылка (напр.: <code>aquaismissing</code>)

Используйте /cancel, чтобы отменить команду."""


### Counter-Strike Xhair code examples
# English
xhair_decode_en = """📖 Please, enter the crosshair code that you would like to decode (ex: <code>CSGO-O4Jsi-V36wY-rTMGK-9w7qF-jQ8WB</code>).

Use /cancel to cancel this command."""

# Russian
xhair_decode_ru = """📖 Пожалуйста, введите код прицела, который желаете расшифровать (напр.: <code>CSGO-O4Jsi-V36wY-rTMGK-9w7qF-jQ8WB</code>).

Используйте /cancel, чтобы отменить команду."""


### Profile information
# English
bans_en = """🔍 <b>General profile information:</b>

• Custom URL: <code>{}</code>
• Steam ID: <code>{}</code>
• Account ID: <code>{}</code>
• Steam2 ID: <code>{}</code>
• Steam3 ID: <code>{}</code>

• Steam friend code: <code>{}</code>
• Steam invite URL: {}
• Counter-Strike friend code: <code>{}</code>

🔫 <b>FACEIT:</b>

• FACEIT URL: {}
• FACEIT elo / level: {}
• FACEIT ban: {}

📛 <b>Bans and restrictions:</b>

• Game bans: {}
• VAC bans: {}
• Community ban: {}
• Trade ban: {}"""

# Russian
bans_ru = """🔍 <b>Общая информация профиля:</b>

• Личная ссылка: {}
• Steam ID: <code>{}</code>
• Account ID: <code>{}</code>
• Steam2 ID: <code>{}</code>
• Steam3 ID: <code>{}</code>

• Код друга Steam: <code>{}</code>
• Пригласительная ссылка Steam: {}
• Код друга Counter-Strike: <code>{}</code>

🔫 <b>FACEIT:</b>

• Ссылка на FACEIT: {}
• Эло на FACEIT / Ранг: {}
• Блокировка FACEIT: {}

📛 <b>Запреты и ограничения:</b>

• Игровые блокировки: {}
• Блокировки VAC: {}
• Блокировка в сообществе: {}
• Ограничение на обмен: {}"""


### Text for Wrong Request
# English
unknownRequest_en = "⚠️ Nothing found, please use one of the following buttons:"

# Russian
unknownRequest_ru = "⚠️ Ничего не найдено, пожалуйста, воспользуйтесь одной из приведённых кнопок:"


### Text for Steam maintenance
# English
maintenance_en = "🛠️ <b>Steam is down for routine maintenance every Tuesday.</b>"

# Russian
maintenance_ru = "🛠️ <b>Steam отключается на плановое техобслуживание каждый вторник.</b>"


### Text if Something's is wrong
# English
wrongBOT_en = "🧐 Sorry, something went wrong. Please, try again later."

# Russian
wrongBOT_ru = "🧐 Извините, пошло что-то не так. Пожалуйста, попробуйте позже."


### Text for Guns
# English
gun_data_en = """🗂 Detailed information about {}:

• Origin: {}
• Cost: ${}
• Clip size: {}/{}
• Fire rate: {} RPM
• Kill reward: ${}
• Movement speed: {} units

• Armor penetration: {}%
• Range accuracy (stand / crouch): {}m / {}m

• Draw time: {}s
• Reload time: {}s / {}s
(clip ready / fire ready)

💢 Damage information:
(enemy with armor / without armor)

• Head: {} / {}
• Chest and arms: {} / {}
• Stomach: {} / {}
• Legs: {} / {}"""

# Russian
gun_data_ru = """🗂 Детальная информация про {}:

• Происхождение: {}
• Стоимость: {}$
• Обойма: {}/{}
• Скорострельность: {} в/м.
• Награда за убийство: {}$
• Мобильность: {} ед.

• Бронепробиваемость: {}%
• Дальность поражения (стоя / сидя): {} / {} м.

• Время, за которое достаётся оружие: {} с.
• Перезарядка: {} / {} с.
(готовность обоймы / готовность к стрельбе)

💢 Информация об уроне:
(противник в броне / без брони)

• Голова: {} / {}
• Грудь и руки: {} / {}
• Живот: {} / {}
• Ноги: {} / {}"""

### Text for Guns
# English
exchange_rate_en = """💸 Price of one Counter-Strike case key:

🇺🇸 USD: $ {}
🇬🇧 GBP: £ {}
🇪🇺 EUR: {} €
🇷🇺 RUB: {} ₽
🇧🇷 BRL: R$ {}
🇯🇵 JPY: ¥ {}
🇳🇴 NOK: {} kr
🇮🇩 IDR: Rp {}
🇲🇾 MYR: RM {}
🇵🇭 PHP: ₱ {}
🇸🇬 SGD: S$ {}
🇹🇭 THB: ฿ {}
🇻🇳 VND: {} ₫
🇰🇷 KRW: ₩ {}
🇹🇷 TRY: ₺ {}
🇺🇦 UAH: {} ₴
🇲🇽 MXN: Mex$ {}
🇨🇦 CAD: CDN$ {}
🇦🇺 AUD: A$ {}
🇳🇿 NZD: NZ$ {}
🇵🇱 PLN: {} zł
🇨🇭 CHF: CHF {}
🇦🇪 AED: {} AED
🇨🇱 CLP: CLP$ {}
🇨🇳 CNY: ¥ {}
🇨🇴 COP: COL$ {}
🇵🇪 PEN: S/. {}
🇸🇦 SAR: {} SR
🇹🇼 TWD: NT$ {}
🇭🇰 HKD: HK$ {}
🇿🇦 ZAR: R {}
🇮🇳 INR: ₹ {}
🇦🇷 ARS: ARS$ {}
🇨🇷 CRC: ₡ {}
🇮🇱 ILS: ₪ {}
🇰🇼 KWD: {} KD
🇶🇦 QAR: {} QR
🇺🇾 UYU: $U {}
🇰🇿 KZT: {} ₸
"""

# Russian
exchange_rate_ru = """💸 Стоимость одного ключа от кейса Counter-Strike:

🇺🇸 USD: $ {}
🇬🇧 GBP: £ {}
🇪🇺 EUR: {} €
🇷🇺 RUB: {} ₽
🇧🇷 BRL: R$ {}
🇯🇵 JPY: ¥ {}
🇳🇴 NOK: {} kr
🇮🇩 IDR: Rp {}
🇲🇾 MYR: RM {}
🇵🇭 PHP: ₱ {}
🇸🇬 SGD: S$ {}
🇹🇭 THB: ฿ {}
🇻🇳 VND: {} ₫
🇰🇷 KRW: ₩ {}
🇹🇷 TRY: ₺ {}
🇺🇦 UAH: {} ₴
🇲🇽 MXN: Mex$ {}
🇨🇦 CAD: CDN$ {}
🇦🇺 AUD: A$ {}
🇳🇿 NZD: NZ$ {}
🇵🇱 PLN: {} zł
🇨🇭 CHF: CHF {}
🇦🇪 AED: {} AED
🇨🇱 CLP: CLP$ {}
🇨🇳 CNY: ¥ {}
🇨🇴 COP: COL$ {}
🇵🇪 PEN: S/.{}
🇸🇦 SAR: {} SR
🇹🇼 TWD: NT$ {}
🇭🇰 HKD: HK$ {}
🇿🇦 ZAR: R {}
🇮🇳 INR: ₹ {}
🇨🇷 CRC: ₡ {}
🇦🇷 ARS: ARS$ {}
🇮🇱 ILS: ₪ {}
🇰🇼 KWD: {} KD
🇶🇦 QAR: {} QR
🇺🇾 UYU: $U {}
🇰🇿 KZT: {} ₸
"""
