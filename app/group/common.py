import pickle

from telegram.error import BadRequest

from config.common import TG_IN_USE_GROUP
from model.db import User, db_session, commit, BotCommand


def check_group_auth(group_id):
    return int(TG_IN_USE_GROUP) == group_id


def check_user_in_group(bot, group_id, user_id):
    try:
        cm = bot.get_chat_member(group_id, user_id)
        if cm.status in ('creator', 'administrator', 'member'):
            return True
    except BadRequest:
        return False


def insert_user_by_update(update):
    with db_session:
        user_id = update.message.from_user.id
        query = User.select(lambda p: p.tg_user_id == user_id)
        if not list(query):
            User(tg_user_id=update.message.from_user.id,
                 tg_user_username=update.message.from_user.username,
                 tg_user_nickname="{} {}".format(update.message.from_user.first_name,
                                                 "" if not update.message.from_user.last_name
                                                 else update.message.from_user.last_name),
                 tg_user_ignore=0)
            commit()


def check_user_in_db(user_id):
    with db_session:
        query = User.select(lambda p: p.tg_user_id == user_id)
        if not list(query):
            return False
        return True


def change_user_ignore(update):
    with db_session:
        user_id = update.message.from_user.id
        user = User.get(tg_user_id=user_id)
        if not user:
            insert_user_by_update(update)
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


def group_auth(func):
    def wrapper(*args, **kwargs):
        bot = args[0]
        update = args[1]
        group_id = update.message.chat.id
        if check_group_auth(group_id):
            func(*args, **kwargs)
        else:
            pass

    return wrapper


def check_in_group_message(func):
    def wrapper(*args, **kwargs):
        bot = args[0]
        update = args[1]
        chat_type = update.message.chat.type
        if chat_type in ("group", "supergroup"):
            update.message.reply_text(text="为减少对群消息的打扰，请通过与 @yuequnbot 私聊来获取信息")
        else:
            func(*args, **kwargs)

    return wrapper


def log_command(func):
    def wrapper(*args, **kwargs):
        bot = args[0]
        update = args[1]

        with db_session:
            BotCommand(tg_user_id=update.message.from_user.id,
                       tg_cmd_timestamp=update.message.date,
                       tg_cmd_text=update.message.text,
                       tg_update_id=update.update_id,
                       tg_update_full=pickle.dumps(update))
            commit()
        func(*args, **kwargs)
    return wrapper
