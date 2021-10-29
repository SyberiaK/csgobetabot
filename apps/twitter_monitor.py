import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from tweepy import StreamListener, Stream, OAuthHandler
import telebot
import logging
import json
import re
import time


import config
from plugins import strings


auth = OAuthHandler(config.TWITTER_API_KEY, config.TWITTER_API_KEY_S)
auth.set_access_token(config.TWITTER_TOKEN, config.TWITTER_TOKEN_S)


class CSGOTwitterListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        if 'user' in tweet and tweet['user']['id_str'] == config.CSGO_TWITTER_ID:
            clean_tweet = re.sub(r' http\S+', '', tweet['text'])
            text_en = strings.notiNewTweet_en.format(clean_tweet, tweet['id'])
            text_ru = strings.notiNewTweet_ru.format(clean_tweet, tweet['id'])
            if not config.TEST_MODE:
                chat_list = [config.CSGOBETACHAT, config.CSGOBETACHAT_EN]
            else:
                chat_list = [config.AQ]
            bot = telebot.TeleBot(config.BOT_TOKEN)
            for chatID in chat_list:
                if chatID == config.CSGOBETACHAT_EN:
                    msg = bot.send_message(chatID, text_en, parse_mode='html')
                else:
                    msg = bot.send_message(chatID, text_ru, parse_mode='html')
                bot.pin_chat_message(msg.chat.id, msg.id,
                                    disable_notification=True)
        else:
            pass

    def on_error(self, status):
        print(status)

    def on_limit(self, status):
        print("Rate Limit Exceeded, Sleep for 15 Mins")
        time.sleep(15 * 60)
        return True


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s | %(message)s', datefmt='%H:%M:%S — %d/%m/%Y')
    l = CSGOTwitterListener()
    twitterStream = Stream(auth, l)
    twitterStream.filter(follow=[config.CSGO_TWITTER_ID])
