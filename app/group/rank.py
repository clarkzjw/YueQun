from pony.orm.core import select, count, desc

from model.db import db_session, Message


def get_rank(args):
    with db_session:
        all_messages = list(select((msg.tg_user_username, count()) for msg in Message).order_by(lambda: desc(count())))
        number = len(all_messages)
        try:
            number = abs(int(args[0]))
        except:
            pass
        rank_text = ""
        c = 1
        for r in all_messages[:number]:
            rank_text += "*{}. {}* => {}\n".format(c, r[0], r[1])
            c += 1
        return rank_text
