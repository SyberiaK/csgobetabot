from steam import steamid
from telegraph import Telegraph
import re
import requests
from steam import steamid
from steam.steamid import SteamID
import requests


import config
from addons.plugins import url_checker
from addons import strings


def csgo_stats(data):
    try:
        steam64 = steamid.from_url(url_checker(data))
        statsURL = f'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?appid={config.CSGO_APP_ID}&key={config.STEAM_API_KEY}&steamid={steam64}'
        response = requests.get(statsURL)
        if response.status_code == 500:
            url_en = '''<a href="https://i.imgur.com/CAjblvT.mp4">‎‎‎‎‎‎‎‎‎‎‎‎</a>❕ This account is private, statistics are not available. Please, change your privacy settings.'''
            url_ru = '''<a href="https://i.imgur.com/CAjblvT.mp4">‎‎‎‎‎‎‎‎‎‎‎‎‎‎</a>❕ Этот аккаунт приватный, невозможно получить статистику. Пожалуйста, поменяйте настройки приватности.'''
        else:
            data = response.json()['playerstats']['stats']
            try:
                totalPlayedTime = int("{:.0f}".format(list(
                    filter(lambda x: x['name'] == 'total_time_played', data))[0]['value'] / 3600))
            except:
                totalPlayedTime = 0
            try:
                totalKills = int(
                    list(filter(lambda x: x['name'] == 'total_kills', data))[0]['value'])
            except:
                totalKills = 0
            try:
                totalDeaths = int(
                    list(filter(lambda x: x['name'] == 'total_deaths', data))[0]['value'])
            except:
                totalDeaths = 0
            if totalKills != 0 and totalDeaths != 0:
                kdRatio = "{:.2f}".format(totalKills / totalDeaths)
            else:
                kdRatio = 0
            try:
                totalRoundsPlayed = int(
                    list(filter(lambda x: x['name'] == 'total_rounds_played', data))[0]['value'])
            except:
                totalRoundsPlayed = 0
            try:
                totalMatchesPlayed = int(
                    list(filter(lambda x: x['name'] == 'total_matches_played', data))[0]['value'])
            except:
                totalMatchesPlayed = 0
            try:
                totalMatchesWon = int(
                    list(filter(lambda x: x['name'] == 'total_matches_won', data))[0]['value'])
            except:
                totalMatchesWon = 0
            try:
                totalPistolRoundsWon = int(
                    list(filter(lambda x: x['name'] == 'total_wins_pistolround', data))[0]['value'])
            except:
                totalPistolRoundsWon = 0
            if totalMatchesPlayed != 0 and totalMatchesWon != 0:
                matchWinPercentage = "{:.2f}".format(
                    totalMatchesWon / totalMatchesPlayed * 100)
            else:
                matchWinPercentage = 0

            try:
                totalShots = int(
                    list(filter(lambda x: x['name'] == 'total_shots_fired', data))[0]['value'])
            except:
                totalShots = 0
            try:
                totalHits = int(
                    list(filter(lambda x: x['name'] == 'total_shots_hit', data))[0]['value'])
            except:
                totalHits = 0
            if totalHits != 0 and totalShots != 0:
                hitAccuracy = "{:.2f}".format(totalHits / totalShots * 100)
            else:
                hitAccuracy = 0

            map_wins_list = [i for i in data if re.match(
                r'total_wins_map_+', i['name'])]
            round_wins_list = [i for i in data if re.match(
                r'total_rounds_map_+', i['name'])]

            temp_map_name = list(filter(lambda x: x['value'] == max(
                i['value'] for i in map_wins_list), data))[0]['name'].split('_')[-1]
            temp_map_data = [x for x in map_wins_list if x['value'] == max(
                i['value'] for i in map_wins_list)]
            temp_round_data = [
                x for x in round_wins_list if x['name'].endswith(temp_map_name)]
            bestMapWins = temp_map_data[0]['value']
            bestMapRounds = temp_round_data[0]['value']

            bestMapPercentage = "{:.2f}".format(
                bestMapWins / bestMapRounds * 100)
            mapName = temp_map_name.capitalize()

            try:
                totalKillsHS = list(
                    filter(lambda x: x['name'] == 'total_kills_headshot', data))[0]['value']
            except:
                totalKillsHS = 0
            if totalKillsHS != 0 and totalKills != 0:
                hsAccuracy = "{:.2f}".format(totalKillsHS / totalKills * 100)
            else:
                hsAccuracy = 0

            try:
                totalDamageDone = list(
                    filter(lambda x: x['name'] == 'total_damage_done', data))[0]['value']
            except:
                totalDamageDone = 0
            try:
                totalWeaponDonated = list(
                    filter(lambda x: x['name'] == 'total_weapons_donated', data))[0]['value']
            except:
                totalWeaponDonated = 0
            try:
                totalBrokenWindows = list(
                    filter(lambda x: x['name'] == 'total_broken_windows', data))[0]['value']
            except:
                totalBrokenWindows = 0
            try:
                totalBombsPlanted = list(
                    filter(lambda x: x['name'] == 'total_planted_bombs', data))[0]['value']
            except:
                totalBombsPlanted = 0
            try:
                totalMVPs = list(filter(lambda x: x['name'] == 'total_mvps', data))[
                    0]['value']
            except:
                totalMVPs = 0
            try:
                totalBombsDefused = list(
                    filter(lambda x: x['name'] == 'total_defused_bombs', data))[0]['value']
            except:
                totalBombsDefused = 0
            try:
                totalMoneyEarned = list(
                    filter(lambda x: x['name'] == 'total_money_earned', data))[0]['value']
            except:
                totalMoneyEarned = 0
            try:
                totalHostagesResc = list(
                    filter(lambda x: x['name'] == 'total_rescued_hostages', data))[0]['value']
            except:
                totalHostagesResc = 0

            try:
                totalKnifeKills = list(
                    filter(lambda x: x['name'] == 'total_kills_knife', data))[0]['value']
            except:
                totalKnifeKills = 0
            try:
                totalKnifeDuelsWon = list(
                    filter(lambda x: x['name'] == 'total_kills_knife_fight', data))[0]['value']
            except:
                totalKnifeDuelsWon = 0
            try:
                totalKillsEnemyWeapon = list(
                    filter(lambda x: x['name'] == 'total_kills_enemy_weapon', data))[0]['value']
            except:
                totalKillsEnemyWeapon = 0
            try:
                totalKillsEnemyBlinded = list(
                    filter(lambda x: x['name'] == 'total_kills_enemy_blinded', data))[0]['value']
            except:
                totalKillsEnemyBlinded = 0
            try:
                totalKillsZoomedEnemy = list(filter(
                    lambda x: x['name'] == 'total_kills_against_zoomed_sniper', data))[0]['value']
            except:
                totalKillsZoomedEnemy = 0
            try:
                totalHEKills = list(
                    filter(lambda x: x['name'] == 'total_kills_hegrenade', data))[0]['value']
            except:
                totalHEKills = 0
            try:
                totalMolotovKills = list(
                    filter(lambda x: x['name'] == 'total_kills_molotov', data))[0]['value']
            except:
                totalMolotovKills = 0
            try:
                totalZeusShots = list(
                    filter(lambda x: x['name'] == 'total_shots_taser', data))[0]['value']
            except:
                totalZeusShots = 0
            try:
                totalZeusKills = list(
                    filter(lambda x: x['name'] == 'total_kills_taser', data))[0]['value']
            except:
                totalZeusKills = 0
            if totalZeusKills != 0 and totalZeusShots != 0:
                ZeusAccuracy = "{:.2f}".format(
                    totalZeusKills / totalZeusShots * 100)
            else:
                ZeusAccuracy = 0

            try:
                totalAk47Kills = list(filter(lambda x: x['name'] == 'total_kills_ak47', data))[
                    0]['value']
            except:
                totalAk47Kills = 0
            try:
                totalAk47Shots = list(filter(lambda x: x['name'] == 'total_shots_ak47', data))[
                    0]['value']
            except:
                totalAk47Shots = 0
            try:
                totalAk47Hits = list(filter(lambda x: x['name'] == 'total_hits_ak47', data))[
                    0]['value']
            except:
                totalAk47Hits = 0
            if totalAk47Hits != 0 and totalAk47Shots != 0:
                Ak47Accuracy = "{:.2f}".format(
                    totalAk47Hits / totalAk47Shots * 100)
            else:
                Ak47Accuracy = 0

            try:
                totalM4Kills = list(filter(lambda x: x['name'] == 'total_kills_m4a1', data))[
                    0]['value']
            except:
                totalM4Kills = 0
            try:
                totalM4Shots = list(filter(lambda x: x['name'] == 'total_shots_m4a1', data))[
                    0]['value']
            except:
                totalM4Shots = 0
            try:
                totalM4Hits = list(filter(lambda x: x['name'] == 'total_hits_m4a1', data))[
                    0]['value']
            except:
                totalM4Hits = 0

            if totalM4Hits != 0 and totalM4Shots != 0:
                m4Accuracy = "{:.2f}".format(totalM4Hits / totalM4Shots * 100)
            else:
                m4Accuracy = 0

            try:
                totalAWPKills = list(filter(lambda x: x['name'] == 'total_kills_awp', data))[
                    0]['value']
            except:
                totalAWPKills = 0
            try:
                totalAWPShots = list(filter(lambda x: x['name'] == 'total_shots_awp', data))[
                    0]['value']
            except:
                totalAWPShots = 0
            try:
                totalAWPHits = list(filter(lambda x: x['name'] == 'total_hits_awp', data))[
                    0]['value']
            except:
                totalAWPHits = 0
            if totalAWPHits != 0 and totalAWPShots != 0:
                AWPAccuracy = "{:.2f}".format(
                    totalAWPHits / totalAWPShots * 100)
            else:
                AWPAccuracy = 0

            try:
                totalGlockKills = list(
                    filter(lambda x: x['name'] == 'total_kills_glock', data))[0]['value']
            except:
                totalGlockKills = 0
            try:
                totalGlockShots = list(
                    filter(lambda x: x['name'] == 'total_shots_glock', data))[0]['value']
            except:
                totalGlockShots = 0
            try:
                totalGlockHits = list(filter(lambda x: x['name'] == 'total_hits_glock', data))[
                    0]['value']
            except:
                totalGlockHits = 0
            if totalGlockHits != 0 and totalGlockShots != 0:
                GlockAccuracy = "{:.2f}".format(
                    totalGlockHits / totalGlockShots * 100)
            else:
                GlockAccuracy = 0

            try:
                totalUSPKills = list(
                    filter(lambda x: x['name'] == 'total_kills_hkp2000', data))[0]['value']
            except:
                totalUSPKills = 0
            try:
                totalUSPShots = list(
                    filter(lambda x: x['name'] == 'total_shots_hkp2000', data))[0]['value']
            except:
                totalUSPShots = 0
            try:
                totalUSPHits = list(filter(lambda x: x['name'] == 'total_hits_hkp2000', data))[
                    0]['value']
            except:
                totalUSPHits = 0
            if totalUSPHits != 0 and totalUSPShots != 0:
                USPAccuracy = "{:.2f}".format(
                    totalUSPHits / totalUSPShots * 100)
            else:
                USPAccuracy = 0

            try:
                totalP250Kills = list(filter(lambda x: x['name'] == 'total_kills_p250', data))[
                    0]['value']
            except:
                totalP250Kills = 0
            try:
                totalP250Shots = list(filter(lambda x: x['name'] == 'total_shots_p250', data))[
                    0]['value']
            except:
                totalP250Shots = 0
            try:
                totalP250Hits = list(filter(lambda x: x['name'] == 'total_hits_p250', data))[
                    0]['value']
            except:
                totalP250Hits = 0
            if totalP250Hits != 0 and totalP250Shots != 0:
                P250Accuracy = "{:.2f}".format(
                    totalP250Hits / totalP250Shots * 100)
            else:
                P250Accuracy = 0

            try:
                totalDualiesKills = list(
                    filter(lambda x: x['name'] == 'total_kills_elite', data))[0]['value']
            except:
                totalDualiesKills = 0
            try:
                totalDualiesShots = list(
                    filter(lambda x: x['name'] == 'total_shots_elite', data))[0]['value']
            except:
                totalDualiesShots = 0
            try:
                totalDualiesHits = list(
                    filter(lambda x: x['name'] == 'total_hits_elite', data))[0]['value']
            except:
                totalDualiesHits = 0
            if totalDualiesHits != 0 and totalDualiesShots != 0:
                DualiesAccuracy = "{:.2f}".format(
                    totalDualiesHits / totalDualiesShots * 100)
            else:
                DualiesAccuracy = 0

            try:
                totalFiveSevenKills = list(
                    filter(lambda x: x['name'] == 'total_kills_fiveseven', data))[0]['value']
            except:
                totalFiveSevenKills = 0
            try:
                totalFiveSevenShots = list(
                    filter(lambda x: x['name'] == 'total_shots_fiveseven', data))[0]['value']
            except:
                totalFiveSevenShots = 0
            try:
                totalFiveSevenHits = list(
                    filter(lambda x: x['name'] == 'total_hits_fiveseven', data))[0]['value']
            except:
                totalFiveSevenHits = 0
            if totalFiveSevenHits != 0 and totalFiveSevenShots != 0:
                FiveSevenAccuracy = "{:.2f}".format(
                    totalFiveSevenHits / totalFiveSevenShots * 100)
            else:
                FiveSevenAccuracy = 0

            try:
                totalTec9Kills = list(filter(lambda x: x['name'] == 'total_kills_tec9', data))[
                    0]['value']
            except:
                totalTec9Kills = 0
            try:
                totalTec9Shots = list(filter(lambda x: x['name'] == 'total_shots_tec9', data))[
                    0]['value']
            except:
                totalTec9Shots = 0
            try:
                totalTec9Hits = list(filter(lambda x: x['name'] == 'total_hits_tec9', data))[
                    0]['value']
            except:
                totalTec9Hits = 0
            if totalTec9Hits != 0 and totalTec9Shots != 0:
                Tec9Accuracy = "{:.2f}".format(
                    totalTec9Hits / totalTec9Shots * 100)
            else:
                Tec9Accuracy = 0

            try:
                totalDeagleKills = list(
                    filter(lambda x: x['name'] == 'total_kills_deagle', data))[0]['value']
            except:
                totalDeagleKills = 0
            try:
                totalDeagleShots = list(
                    filter(lambda x: x['name'] == 'total_shots_deagle', data))[0]['value']
            except:
                totalDeagleShots = 0
            try:
                totalDeagleHits = list(
                    filter(lambda x: x['name'] == 'total_hits_deagle', data))[0]['value']
            except:
                totalDeagleHits = 0
            if totalDeagleHits != 0 and totalDeagleShots != 0:
                DeagleAccuracy = "{:.2f}".format(
                    totalDeagleHits / totalDeagleShots * 100)
            else:
                DeagleAccuracy = 0

            try:
                totalMac10Kills = list(
                    filter(lambda x: x['name'] == 'total_kills_mac10', data))[0]['value']
            except:
                totalMac10Kills = 0
            try:
                totalMac10Shots = list(
                    filter(lambda x: x['name'] == 'total_shots_mac10', data))[0]['value']
            except:
                totalMac10Shots = 0
            try:
                totalMac10Hits = list(filter(lambda x: x['name'] == 'total_hits_mac10', data))[
                    0]['value']
            except:
                totalMac10Hits = 0
            if totalMac10Hits != 0 and totalMac10Shots != 0:
                Mac10Accuracy = "{:.2f}".format(
                    totalMac10Hits / totalMac10Shots * 100)
            else:
                Mac10Accuracy = 0

            try:
                totalMp7Kills = list(filter(lambda x: x['name'] == 'total_kills_mp7', data))[
                    0]['value']
            except:
                totalMp7Kills = 0
            try:
                totalMp7Shots = list(filter(lambda x: x['name'] == 'total_shots_mp7', data))[
                    0]['value']
            except:
                totalMp7Shots = 0
            try:
                totalMp7Hits = list(filter(lambda x: x['name'] == 'total_hits_mp7', data))[
                    0]['value']
            except:
                totalMp7Hits = 0
            if totalMp7Hits != 0 and totalMp7Shots != 0:
                Mp7Accuracy = "{:.2f}".format(
                    totalMp7Hits / totalMp7Shots * 100)
            else:
                Mp7Accuracy = 0

            try:
                totalMp9Kills = list(filter(lambda x: x['name'] == 'total_kills_mp9', data))[
                    0]['value']
            except:
                totalMp9Kills = 0
            try:
                totalMp9Shots = list(filter(lambda x: x['name'] == 'total_shots_mp9', data))[
                    0]['value']
            except:
                totalMp9Shots = 0
            try:
                totalMp9Hits = list(filter(lambda x: x['name'] == 'total_hits_mp9', data))[
                    0]['value']
            except:
                totalMp9Hits = 0
            if totalMp9Hits != 0 and totalMp9Shots != 0:
                Mp9Accuracy = "{:.2f}".format(
                    totalMp9Hits / totalMp9Shots * 100)
            else:
                Mp9Accuracy = 0

            try:
                totalUMPKills = list(filter(lambda x: x['name'] == 'total_kills_ump45', data))[
                    0]['value']
            except:
                totalUMPKills = 0
            try:
                totalUMPShots = list(filter(lambda x: x['name'] == 'total_shots_ump45', data))[
                    0]['value']
            except:
                totalUMPShots = 0
            try:
                totalUMPHits = list(filter(lambda x: x['name'] == 'total_hits_ump45', data))[
                    0]['value']
            except:
                totalUMPHits = 0
            if totalUMPHits != 0 and totalUMPShots != 0:
                UMPAccuracy = "{:.2f}".format(
                    totalUMPHits / totalUMPShots * 100)
            else:
                UMPAccuracy = 0

            try:
                totalBizonKills = list(
                    filter(lambda x: x['name'] == 'total_kills_bizon', data))[0]['value']
            except:
                totalBizonKills = 0
            try:
                totalBizonShots = list(
                    filter(lambda x: x['name'] == 'total_shots_bizon', data))[0]['value']
            except:
                totalBizonShots = 0
            try:
                totalBizonHits = list(filter(lambda x: x['name'] == 'total_hits_bizon', data))[
                    0]['value']
            except:
                totalBizonHits = 0
            if totalBizonHits != 0 and totalBizonShots != 0:
                BizonAccuracy = "{:.2f}".format(
                    totalBizonHits / totalBizonShots * 100)
            else:
                BizonAccuracy = 0

            try:
                totalP90Kills = list(filter(lambda x: x['name'] == 'total_kills_p90', data))[
                    0]['value']
            except:
                totalP90Kills = 0
            try:
                totalP90Shots = list(filter(lambda x: x['name'] == 'total_shots_p90', data))[
                    0]['value']
            except:
                totalP90Shots = 0
            try:
                totalP90Hits = list(filter(lambda x: x['name'] == 'total_hits_p90', data))[
                    0]['value']
            except:
                totalP90Hits = 0
            if totalP90Hits != 0 and totalP90Shots != 0:
                P90Accuracy = "{:.2f}".format(
                    totalP90Hits / totalP90Shots * 100)
            else:
                FamasAccuracy = 0

            try:
                totalFamasKills = list(
                    filter(lambda x: x['name'] == 'total_kills_famas', data))[0]['value']
            except:
                totalFamasKills = 0
            try:
                totalFamasShots = list(
                    filter(lambda x: x['name'] == 'total_shots_famas', data))[0]['value']
            except:
                totalFamasShots = 0
            try:
                totalFamasHits = list(filter(lambda x: x['name'] == 'total_hits_famas', data))[
                    0]['value']
            except:
                totalFamasHits = 0
            if totalFamasHits != 0 and totalFamasShots != 0:
                FamasAccuracy = "{:.2f}".format(
                    totalFamasHits / totalFamasShots * 100)
            else:
                FamasAccuracy = 0

            try:
                totalGalilKills = list(
                    filter(lambda x: x['name'] == 'total_kills_galilar', data))[0]['value']
            except:
                totalGalilKills = 0
            try:
                totalGalilShots = list(
                    filter(lambda x: x['name'] == 'total_shots_galilar', data))[0]['value']
            except:
                totalGalilShots = 0
            try:
                totalGalilHits = list(
                    filter(lambda x: x['name'] == 'total_hits_galilar', data))[0]['value']
            except:
                totalGalilHits = 0
            if totalGalilHits != 0 and totalGalilShots != 0:
                GalilAccuracy = "{:.2f}".format(
                    totalGalilHits / totalGalilShots * 100)
            else:
                GalilAccuracy = 0

            try:
                totalAugKills = list(filter(lambda x: x['name'] == 'total_kills_aug', data))[
                    0]['value']
            except:
                totalAugKills = 0
            try:
                totalAugShots = list(filter(lambda x: x['name'] == 'total_shots_aug', data))[
                    0]['value']
            except:
                totalAugShots = 0
            try:
                totalAugHits = list(filter(lambda x: x['name'] == 'total_hits_aug', data))[
                    0]['value']
            except:
                totalAugHits = 0
            if totalAugHits != 0 and totalAugShots != 0:
                AugAccuracy = "{:.2f}".format(
                    totalAugHits / totalAugShots * 100)
            else:
                AugAccuracy = 0

            try:
                totalSgKills = list(filter(lambda x: x['name'] == 'total_kills_sg556', data))[
                    0]['value']
            except:
                totalSgKills = 0
            try:
                totalSgShots = list(filter(lambda x: x['name'] == 'total_shots_sg556', data))[
                    0]['value']
            except:
                totalSgShots = 0
            try:
                totalSgHits = list(filter(lambda x: x['name'] == 'total_hits_sg556', data))[
                    0]['value']
            except:
                totalSgHits = 0
            if totalSgHits != 0 and totalSgShots != 0:
                SgAccuracy = "{:.2f}".format(totalSgHits / totalSgShots * 100)
            else:
                SgAccuracy = 0

            try:
                totalSsgKills = list(filter(lambda x: x['name'] == 'total_kills_ssg08', data))[
                    0]['value']
            except:
                totalSsgKills = 0
            try:
                totalSsgShots = list(filter(lambda x: x['name'] == 'total_shots_ssg08', data))[
                    0]['value']
            except:
                totalSsgShots = 0
            try:
                totalSsgHits = list(filter(lambda x: x['name'] == 'total_hits_ssg08', data))[
                    0]['value']
            except:
                totalSsgHits = 0
            if totalSsgHits != 0 and totalSsgShots != 0:
                SsgAccuracy = "{:.2f}".format(
                    totalSsgHits / totalSsgShots * 100)
            else:
                SsgAccuracy = 0

            try:
                totalScarKills = list(
                    filter(lambda x: x['name'] == 'total_kills_scar20', data))[0]['value']
            except:
                totalScarKills = 0
            try:
                totalScarShots = list(
                    filter(lambda x: x['name'] == 'total_shots_scar20', data))[0]['value']
            except:
                totalScarShots = 0
            try:
                totalScarHits = list(filter(lambda x: x['name'] == 'total_hits_scar20', data))[
                    0]['value']
            except:
                totalScarHits = 0
            if totalScarHits != 0 and totalScarShots != 0:
                ScarAccuracy = "{:.2f}".format(
                    totalScarHits / totalScarShots * 100)
            else:
                ScarAccuracy = 0

            try:
                totalG3SGKills = list(
                    filter(lambda x: x['name'] == 'total_kills_g3sg1', data))[0]['value']
            except:
                totalG3SGKills = 0
            try:
                totalG3SGShots = list(
                    filter(lambda x: x['name'] == 'total_shots_g3sg1', data))[0]['value']
            except:
                totalG3SGShots = 0
            try:
                totalG3SGHits = list(filter(lambda x: x['name'] == 'total_hits_g3sg1', data))[
                    0]['value']
            except:
                totalG3SGHits = 0
            if totalG3SGHits != 0 and totalG3SGShots != 0:
                G3SGAccuracy = "{:.2f}".format(
                    totalG3SGHits / totalG3SGShots * 100)
            else:
                G3SGAccuracy = 0

            try:
                totalNovaKills = list(filter(lambda x: x['name'] == 'total_kills_nova', data))[
                    0]['value']
            except:
                totalNovaKills = 0
            try:
                totalNovaShots = list(filter(lambda x: x['name'] == 'total_shots_nova', data))[
                    0]['value']
            except:
                totalNovaShots = 0
            try:
                totalNovaHits = list(filter(lambda x: x['name'] == 'total_hits_nova', data))[
                    0]['value']
            except:
                totalNovaHits = 0
            if totalNovaHits != 0 and totalNovaShots != 0:
                NovaAccuracy = "{:.2f}".format(
                    totalNovaHits / totalNovaShots * 100)
            else:
                Mag7Accuracy = 0

            try:
                totalMag7Kills = list(filter(lambda x: x['name'] == 'total_kills_mag7', data))[
                    0]['value']
            except:
                totalMag7Kills = 0
            try:
                totalMag7Shots = list(filter(lambda x: x['name'] == 'total_shots_mag7', data))[
                    0]['value']
            except:
                totalMag7Shots = 0
            try:
                totalMag7Hits = list(filter(lambda x: x['name'] == 'total_hits_mag7', data))[
                    0]['value']
            except:
                totalMag7Hits = 0
            if totalMag7Hits != 0 and totalMag7Shots != 0:
                Mag7Accuracy = "{:.2f}".format(
                    totalMag7Hits / totalMag7Shots * 100)
            else:
                Mag7Accuracy = 0

            try:
                totalSawedoffKills = list(
                    filter(lambda x: x['name'] == 'total_kills_sawedoff', data))[0]['value']
            except:
                totalSawedoffKills = 0
            try:
                totalSawedoffShots = list(
                    filter(lambda x: x['name'] == 'total_shots_sawedoff', data))[0]['value']
            except:
                totalSawedoffShots = 0
            try:
                totalSawedoffHits = list(
                    filter(lambda x: x['name'] == 'total_hits_sawedoff', data))[0]['value']
            except:
                totalSawedoffHits = 0
            if totalSawedoffHits != 0 and totalSawedoffShots != 0:
                SawedoffAccuracy = "{:.2f}".format(
                    totalSawedoffHits / totalSawedoffShots * 100)
            else:
                SawedoffAccuracy = 0

            try:
                totalXm1014Kills = list(
                    filter(lambda x: x['name'] == 'total_kills_xm1014', data))[0]['value']
            except:
                totalXm1014Kills = 0
            try:
                totalXm1014Shots = list(
                    filter(lambda x: x['name'] == 'total_shots_xm1014', data))[0]['value']
            except:
                totalXm1014Shots = 0
            try:
                totalXm1014Hits = list(
                    filter(lambda x: x['name'] == 'total_hits_xm1014', data))[0]['value']
            except:
                totalXm1014Hits = 0
            if totalXm1014Hits != 0 and totalXm1014Shots != 0:
                Xm1014Accuracy = "{:.2f}".format(
                    totalXm1014Hits / totalXm1014Shots * 100)
            else:
                Xm1014Accuracy = 0

            try:
                totalNegevKills = list(
                    filter(lambda x: x['name'] == 'total_kills_negev', data))[0]['value']
            except:
                totalNegevKills = 0
            try:
                totalNegevShots = list(
                    filter(lambda x: x['name'] == 'total_shots_negev', data))[0]['value']
            except:
                totalNegevShots = 0
            try:
                totalNegevHits = list(filter(lambda x: x['name'] == 'total_hits_negev', data))[
                    0]['value']
            except:
                totalNegevHits = 0
            if totalNegevHits != 0 and totalNegevShots != 0:
                NegevAccuracy = "{:.2f}".format(
                    totalNegevHits / totalNegevShots * 100)
            else:
                NegevAccuracy = 0

            try:
                totalM249Kills = list(filter(lambda x: x['name'] == 'total_kills_m249', data))[
                    0]['value']
            except:
                totalM249Kills = 0
            try:
                totalM249Shots = list(filter(lambda x: x['name'] == 'total_shots_m249', data))[
                    0]['value']
            except:
                totalM249Shots = 0
            try:
                totalM249Hits = list(filter(lambda x: x['name'] == 'total_hits_m249', data))[
                    0]['value']
            except:
                totalM249Hits = 0
            if totalM249Hits != 0 and totalM249Shots != 0:
                M249Accuracy = "{:.2f}".format(
                    totalM249Hits / totalM249Shots * 100)
            else:
                M249Accuracy = 0

            stats_text_en = strings.stats_en.format(totalPlayedTime, totalKills, totalDeaths, kdRatio,
                                                    totalMatchesPlayed, totalMatchesWon, matchWinPercentage, totalRoundsPlayed, totalPistolRoundsWon,
                                                    totalShots, totalHits, hitAccuracy, hsAccuracy,
                                                    mapName, bestMapPercentage,
                                                    totalMVPs, totalMoneyEarned, totalHostagesResc, totalWeaponDonated, totalBrokenWindows,
                                                    totalDamageDone, totalBombsPlanted, totalBombsDefused,
                                                    totalKnifeKills, totalHEKills, totalMolotovKills, totalZeusShots, totalZeusKills, ZeusAccuracy,
                                                    totalKnifeDuelsWon, totalKillsEnemyWeapon, totalKillsEnemyBlinded, totalKillsZoomedEnemy,
                                                    totalAk47Shots, totalAk47Hits, totalAk47Kills, Ak47Accuracy,
                                                    totalM4Shots, totalM4Hits, totalM4Kills, m4Accuracy,
                                                    totalAWPShots, totalAWPHits, totalAWPKills, AWPAccuracy,
                                                    totalGlockShots, totalGlockHits, totalGlockKills, GlockAccuracy,
                                                    totalUSPShots, totalUSPHits, totalUSPKills, USPAccuracy,
                                                    totalP250Shots, totalP250Hits, totalP250Kills, P250Accuracy,
                                                    totalDualiesShots, totalDualiesHits, totalDualiesKills, DualiesAccuracy,
                                                    totalFiveSevenShots, totalFiveSevenHits, totalFiveSevenKills, FiveSevenAccuracy,
                                                    totalTec9Shots, totalTec9Hits, totalTec9Kills, Tec9Accuracy,
                                                    totalDeagleShots, totalDeagleHits, totalDeagleKills, DeagleAccuracy,
                                                    totalMac10Shots, totalMac10Hits, totalMac10Kills, Mac10Accuracy,
                                                    totalMp7Shots, totalMp7Hits, totalMp7Kills, Mp7Accuracy,
                                                    totalMp9Shots, totalMp9Hits, totalMp9Kills, Mp9Accuracy,
                                                    totalUMPShots, totalUMPHits, totalUMPKills, UMPAccuracy,
                                                    totalBizonShots, totalBizonHits, totalBizonKills, BizonAccuracy,
                                                    totalP90Shots, totalP90Hits, totalP90Kills, P90Accuracy,
                                                    totalFamasShots, totalFamasHits, totalFamasKills, FamasAccuracy,
                                                    totalGalilShots, totalGalilHits, totalGalilKills, GalilAccuracy,
                                                    totalAugShots, totalAugHits, totalAugKills, AugAccuracy,
                                                    totalSgShots, totalSgHits, totalSgKills, SgAccuracy,
                                                    totalSsgShots, totalSsgHits, totalSsgKills, SsgAccuracy,
                                                    totalScarShots, totalScarHits, totalScarKills, ScarAccuracy,
                                                    totalG3SGShots, totalG3SGHits, totalG3SGKills, G3SGAccuracy,
                                                    totalNovaShots, totalNovaHits, totalNovaKills, NovaAccuracy,
                                                    totalMag7Shots, totalMag7Hits, totalMag7Kills, Mag7Accuracy,
                                                    totalSawedoffShots, totalSawedoffHits, totalSawedoffKills, SawedoffAccuracy,
                                                    totalXm1014Shots, totalXm1014Hits, totalXm1014Kills, Xm1014Accuracy,
                                                    totalNegevShots, totalNegevHits, totalNegevKills, NegevAccuracy,
                                                    totalM249Shots, totalM249Hits, totalM249Kills, M249Accuracy)

            stats_text_ru = strings.stats_ru.format(totalPlayedTime, totalKills, totalDeaths, kdRatio,
                                                    totalMatchesPlayed, totalMatchesWon, matchWinPercentage, totalRoundsPlayed, totalPistolRoundsWon,
                                                    totalShots, totalHits, hitAccuracy, hsAccuracy,
                                                    mapName, bestMapPercentage,
                                                    totalMVPs, totalMoneyEarned, totalHostagesResc, totalWeaponDonated, totalBrokenWindows,
                                                    totalDamageDone, totalBombsPlanted, totalBombsDefused,
                                                    totalKnifeKills, totalHEKills, totalMolotovKills, totalZeusShots, totalZeusKills, ZeusAccuracy,
                                                    totalKnifeDuelsWon, totalKillsEnemyWeapon, totalKillsEnemyBlinded, totalKillsZoomedEnemy,
                                                    totalAk47Shots, totalAk47Hits, totalAk47Kills, Ak47Accuracy,
                                                    totalM4Shots, totalM4Hits, totalM4Kills, m4Accuracy,
                                                    totalAWPShots, totalAWPHits, totalAWPKills, AWPAccuracy,
                                                    totalGlockShots, totalGlockHits, totalGlockKills, GlockAccuracy,
                                                    totalUSPShots, totalUSPHits, totalUSPKills, USPAccuracy,
                                                    totalP250Shots, totalP250Hits, totalP250Kills, P250Accuracy,
                                                    totalDualiesShots, totalDualiesHits, totalDualiesKills, DualiesAccuracy,
                                                    totalFiveSevenShots, totalFiveSevenHits, totalFiveSevenKills, FiveSevenAccuracy,
                                                    totalTec9Shots, totalTec9Hits, totalTec9Kills, Tec9Accuracy,
                                                    totalDeagleShots, totalDeagleHits, totalDeagleKills, DeagleAccuracy,
                                                    totalMac10Shots, totalMac10Hits, totalMac10Kills, Mac10Accuracy,
                                                    totalMp7Shots, totalMp7Hits, totalMp7Kills, Mp7Accuracy,
                                                    totalMp9Shots, totalMp9Hits, totalMp9Kills, Mp9Accuracy,
                                                    totalUMPShots, totalUMPHits, totalUMPKills, UMPAccuracy,
                                                    totalBizonShots, totalBizonHits, totalBizonKills, BizonAccuracy,
                                                    totalP90Shots, totalP90Hits, totalP90Kills, P90Accuracy,
                                                    totalFamasShots, totalFamasHits, totalFamasKills, FamasAccuracy,
                                                    totalGalilShots, totalGalilHits, totalGalilKills, GalilAccuracy,
                                                    totalAugShots, totalAugHits, totalAugKills, AugAccuracy,
                                                    totalSgShots, totalSgHits, totalSgKills, SgAccuracy,
                                                    totalSsgShots, totalSsgHits, totalSsgKills, SsgAccuracy,
                                                    totalScarShots, totalScarHits, totalScarKills, ScarAccuracy,
                                                    totalG3SGShots, totalG3SGHits, totalG3SGKills, G3SGAccuracy,
                                                    totalNovaShots, totalNovaHits, totalNovaKills, NovaAccuracy,
                                                    totalMag7Shots, totalMag7Hits, totalMag7Kills, Mag7Accuracy,
                                                    totalSawedoffShots, totalSawedoffHits, totalSawedoffKills, SawedoffAccuracy,
                                                    totalXm1014Shots, totalXm1014Hits, totalXm1014Kills, Xm1014Accuracy,
                                                    totalNegevShots, totalNegevHits, totalNegevKills, NegevAccuracy,
                                                    totalM249Shots, totalM249Hits, totalM249Kills, M249Accuracy)

            telegraph = Telegraph(access_token=config.TELEGRAPH_ACCESS_TOKEN)

            telegraph_response_en = telegraph.create_page(
                f'Statistics #{steam64}', html_content=stats_text_en, author_name='@csgobetabot', author_url='https://t.me/csgobetabot')
            telegraph_response_ru = telegraph.create_page(
                f'Статистика #{steam64}', html_content=stats_text_ru, author_name='@csgobetabot', author_url='https://t.me/csgobetabot')

            url_en = telegraph_response_en['url']
            url_ru = telegraph_response_ru['url']

        return url_en, url_ru
    except Exception as e:
        print('\n\nError:' + str(e) + '\n\n')
        url_en, url_ru = '⚠️ Invalid request.', '⚠️ Неверный запрос.'
        return url_en, url_ru



def ban_info(data):
    try:
        steam64 = steamid.from_url(url_checker(data))

        bans = f'http://api.steampowered.com/ISteamUser/GetPlayerBans/v1?key={config.STEAM_API_KEY}&steamids={steam64}'
        vanity = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={config.STEAM_API_KEY}&steamids={steam64}'
        faceitAPI = f'https://api.faceit.com/search/v2/players?query={steam64}'

        vanityURL = requests.get(vanity).json(
        )['response']['players'][0]['profileurl'].split('/')[-2]
        steamID = SteamID(steam64).as_64
        if vanityURL == str(steamID):
            vanityURL = 'not set'
            vanityURLR = 'не указана'
        else:
            vanityURLR = vanityURL
        accountID = SteamID(steam64).id
        steam2ID = SteamID(steam64).as_steam2
        steam3ID = SteamID(steam64).as_steam3
        inviteUrl = SteamID(steam64).invite_url
        csgoCode = SteamID(steam64).as_csgo_friend_code

        responseFaceit = requests.get(faceitAPI).json()['payload']['results']
        if responseFaceit:
            resultFaceit = list(filter(lambda x: [i for i in x['games'] if i['name'] == 'csgo'], responseFaceit))[0]
            faceitURL = faceitURLR = 'https://faceit.com/en/players/{}'.format(resultFaceit['nickname'])
            if 'banned' in resultFaceit['status']:
                faceitBan = 'banned'
                faceitBanR = 'заблокирован'
            else:
                faceitBan = 'none'
                faceitBanR = 'нет'
            
            for i in resultFaceit['games']:
                if i['name'] == 'csgo':
                    faceitURL = faceitURL + '\n' + '• FACEIT level: ' + str(i['skill_level'])
                    faceitURLR = faceitURLR + '\n' + '• Ранг FACEIT: ' + str(i['skill_level'])
        else:
            faceitURL = 'not found'
            faceitURLR = 'не найдена'

            faceitBan = 'none'
            faceitBanR = 'нет'
        
        banData = requests.get(bans).json()['players'][0]
        if banData['VACBanned']:
            vacBan = str(banData['NumberOfVACBans']) + \
                ' (days since last ban: ' + \
                str(banData['DaysSinceLastBan']) + ')'
            vacBanR = str(banData['NumberOfVACBans']) + \
                ' (дней с момента последней блокировки: ' + \
                str(banData['DaysSinceLastBan']) + ')'
        else:
            vacBan = 0
            vacBanR = 0
        gameBans = banData['NumberOfGameBans']
        if banData['CommunityBanned']:
            communityBan = 'banned'
            communityBanR = 'заблокирован'
        else:
            communityBan = 'none'
            communityBanR = 'нет'
        if banData['EconomyBan'] == 'banned':
            tradeBan = 'banned'
            tradeBanR = 'заблокирован'
        else:
            tradeBan = 'none'
            tradeBanR = 'нет'

        bans_text_en = strings.bans_en.format(vanityURL, steamID, accountID, steam2ID, steam3ID, inviteUrl,
                                              csgoCode, faceitURL, gameBans, vacBan, communityBan, tradeBan, faceitBan)
        bans_text_ru = strings.bans_ru.format(vanityURLR, steamID, accountID, steam2ID, steam3ID, inviteUrl,
                                              csgoCode, faceitURLR, gameBans, vacBanR, communityBanR, tradeBanR, faceitBanR)
        return bans_text_en, bans_text_ru
    except Exception as e:
        print('\n\nError:' + str(e) + '\n\n')
        bans_text_en, bans_text_ru = '⚠️ Invalid request.', '⚠️ Неверный запрос.'
        return bans_text_en, bans_text_ru
