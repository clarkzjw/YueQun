from pony.orm.core import select, count, desc

from model.db import db_session, Message


def get_rank():
    with db_session:
        all_messages = list(select((msg.tg_user_username, count()) for msg in Message).order_by(lambda: desc(count())))
        rank_text = ""
        c = 1
        for r in all_messages:
            rank_text += "*{}. {}* => {}\n".format(c, r[0], r[1])
            c += 1
        return rank_text
