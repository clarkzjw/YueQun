from pony.orm.core import select
from telegram import ParseMode

from group.parse import get_update_text
from model.db import db_session, Reminder, commit, delete


def set_keyword_reminder(user_id, args):
    with db_session:
        for w in args:
            word = list(select(r.keyword for r in Reminder if r.keyword == str(w) and r.tg_user_id == user_id))
            if not word:
                Reminder(keyword=str(w),
                         tg_user_id=user_id)
                commit()
        keywords = list(select(r.keyword for r in Reminder if r.tg_user_id == user_id))
        return "您的关键词设置成功，当前共有以下关键词：{}".format(keywords)


def user_del_keyword(user_id, args):
    with db_session:
        for w in args:
            word = list(select(r.keyword for r in Reminder if r.keyword == str(w) and r.tg_user_id == user_id))
            if not word:
                continue
            delete(r for r in Reminder if r.keyword == str(w) and r.tg_user_id == user_id)
        keywords = list(select(r.keyword for r in Reminder if r.tg_user_id == user_id))
    return "您的关键词删除成功，当前共有以下关键词：{}".format(keywords)


def get_keyword_by_user_id(user_id):
    with db_session:
        keywords = list(select(r.keyword for r in Reminder if r.tg_user_id == user_id))
        if not keywords:
            return "您当前设置的关键词为空"
        else:
            return "您当前设置的关键词有：{}".format(str(keywords))


def send_keyword_notify(bot, update, keyword):
    try:
        msg = "{}, `{}` 在水群中提到了 `{}`".format(update.message.date, update.message.from_user.username, keyword[0])
        bot.send_message(chat_id=keyword[1], text=msg, parse_mode=ParseMode.MARKDOWN)
        bot.forward_message(chat_id=keyword[1],
                            from_chat_id=update.message.chat_id,
                            message_id=update.message.message_id)
    except Exception as e:
        print(e)


def check_keyword_and_sent(bot, update):
    text = get_update_text(update)
    if not text:
        return
    with db_session:
        db_keywords = list(select((r.keyword, r.tg_user_id) for r in Reminder))
        for word in db_keywords:
            if word[0] in text:
                send_keyword_notify(bot, update, word)
