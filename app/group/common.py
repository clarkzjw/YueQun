from telegram.error import BadRequest

from config.common import TG_IN_USE_GROUP
from model.db import User, db_session, commit


def check_group_auth(group_id):
    return int(TG_IN_USE_GROUP) == group_id


def get_group_member_list(bot, group_id):
    pass


def check_user_in_group(bot, group_id, user_id):
    try:
        cm = bot.get_chat_member(group_id, user_id)
        if cm.status in ('creator', 'administrator', 'member'):
            return True
    except BadRequest:
        return False


def insert_user_in_db(user_id):
    with db_session:
        User(tg_user_id=user_id)
        commit()


def check_user_in_db(user_id):
    with db_session:
        query = User.select(lambda p: p.tg_user_id == user_id)
        if not list(query):
            return False
        return True


def change_user_ignore(user_id):
    with db_session:
        user = User.get(tg_user_id=user_id)
        if not user:
            insert_user_in_db(user_id)
        user = User.get(tg_user_id=user_id)
        user.tg_user_ignore = 1 ^ user.tg_user_ignore
        commit()
        return user.tg_user_ignore


def Unauthorized(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text(text="您尚未加入杭蓝水群，请联系您周围的友军！")


def auth(func):
    def wrapper(*args, **kwargs):
        bot = args[0]
        update = args[1]
        user_id = update.message.from_user.id
        if check_user_in_group(bot, TG_IN_USE_GROUP, user_id):
            func(*args, **kwargs)
        else:
            Unauthorized(*args, **kwargs)

    return wrapper