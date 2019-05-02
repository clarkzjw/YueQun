from db.model import User, db_session


def check_is_mention(update):
    for e in update.message.entities:
        if e.type == "mention":
            return 1
    return 0


def check_is_reply(update):
    if hasattr(update.message, 'reply_to_message') is True and update.message.reply_to_message is not None:
        return 1
    return 0


def check_is_sticker(update):
    if hasattr(update.message, "sticker") is True and update.message.sticker is not None:
        return 1
    return 0


def get_update_text(update):
    try:
        return update.message.text
    except:
        return None


def check_user_ignore(update):
    user_id = update.message.from_user.id
    with db_session:
        query = User.select(lambda p: p.tg_user_id == user_id)

        if not list(query):
            return False
        user = list(query)
        if user[0].tg_user_ignore is True:
            return True
        return False

