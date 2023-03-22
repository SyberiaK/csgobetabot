import env

import logging
import multiprocessing.dummy

import config
import ratelimitqueue
import requests
import telebot
from addons import file_manager
from strings import notifications

HIDDEN_IDS = []
PUBLIC_IDS = []

BASE_URL = "https://blog.counter-strike.net/wp-json/wp/v2/posts/{}"
hdrs = {
    "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"
}

sesh = requests.Session()
rlq = ratelimitqueue.RateLimitQueue(calls=2, per=0, fuzz=1)
n_workers = 2


def main():
    while True:
        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        blogID = cacheFile["last_blog_id"]
        LIST_OF_URLS = [BASE_URL.format(i) for i in range(blogID + 1, blogID + 151)]

        for url in LIST_OF_URLS:
            rlq.put(url)

        with multiprocessing.dummy.Pool(n_workers, worker, (rlq,)) as pool:
            rlq.join()
            check_ids()


def worker(rlq):
    while rlq.qsize() > 0:
        url = rlq.get()
        make_call(url)
        rlq.task_done()


def make_call(url):
    try:
        resp = sesh.get(url, headers=hdrs, timeout=15)
        if resp.status_code == 401:
            HIDDEN_IDS.append(int(url.split("/")[-1]))
        elif resp.status_code == 200:
            PUBLIC_IDS.append(int(url.split("/")[-1]))
    except Exception as e:
        print(f"\n\nError: {e}\n\n")


def check_ids():
    HIDDEN_IDS.sort()
    PUBLIC_IDS.sort()
    if HIDDEN_IDS:
        send_alert(HIDDEN_IDS)
        file_manager.updateJson(config.CACHE_FILE_PATH, HIDDEN_IDS[-1], "last_blog_id")
    elif PUBLIC_IDS:
        file_manager.updateJson(config.CACHE_FILE_PATH, PUBLIC_IDS[-1], "last_blog_id")
    HIDDEN_IDS.clear()
    PUBLIC_IDS.clear()


def send_alert(data):
    bot = telebot.TeleBot(config.BOT_TOKEN)

    if len(data) < 2:
        text_ru = notifications.hiddenPost.format(*data)
        text_en = f"🔍 New hidden CS:GO blog post found!\n\nID: {data[0]}"
    else:
        posts = " и ".join(
            map(
                str,
                [", ".join(map(str, data[:-1])), data[-1]] if len(data) > 2 else data,
            )
        )
        text_ru = notifications.hiddenPosts.format(posts)
        text_en = (
            f"🔍 New hidden CS:GO blog posts found!\n\nIDs: {posts.replace('и', 'and')}"
        )

    if not config.TEST_MODE:
        chatID = config.CSGOBETACHAT
        bot.send_message(config.AQ_TRACKER, text_en)
    else:
        chatID = config.AQ

    msg = bot.send_message(chatID, text_ru, disable_web_page_preview=True, parse_mode="html")
    if chatID == config.CSGOBETACHAT:
        bot.pin_chat_message(msg.chat.id, msg.id, disable_notification=True)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(message)s",
        datefmt="%H:%M:%S — %d/%m/%Y",
    )
    main()
