import csv
import unicodedata

import jieba
import jieba.analyse
import validators
from emoji import UNICODE_EMOJI
from pony.orm.core import select
from wordcloud import WordCloud

from model.db import db_session, Message

stopwords = set()


def is_emoji(s):
    return s in UNICODE_EMOJI


def get_word_cloud():
    for i in open("/yqbot/app/stopwords.txt").read().split('\n'):
        stopwords.add(unicodedata.normalize('NFC', i))

    with db_session:
        all_messages = list(select(msg.tg_msg_text for msg in Message))
        words = {}
        for msg in all_messages:
            if validators.url(msg):
                continue

            for w in jieba.cut(msg, cut_all=False):
                w = unicodedata.normalize('NFC', w)
                w = w.strip()
                if not w:
                    continue
                if w in stopwords:
                    continue
                if is_emoji(w):
                    continue
                if w not in words:
                    words[w] = 1
                else:
                    words[w] += 1

    with open('cut_result.csv', 'w') as cf:
        writer = csv.DictWriter(cf, ["word", "count"])
        writer.writeheader()
        for w in sorted(words, key=words.get, reverse=True):
            writer.writerow({"word": w, "count": words[w]})

    wd = {}

    with open("cut_result.csv") as f:
        reader = csv.DictReader(f)
        for i in reader:
            wd[i["word"]] = int(i["count"])

    wordcloud = WordCloud(width=1024, height=1024, font_path="/Library/Fonts/SourceHanSans-Normal.ttc",
                          color_func=lambda *args, **kwargs: (140, 184, 255)).generate_from_frequencies(wd)

    image = wordcloud.to_image()
    return image
