from pony.orm.core import select, count, desc

from model.db import db_session, Message, User


def get_rank(args):
    with db_session:
        all_users = list(select((user.tg_user_id, user.tg_user_username) for user in User))
        users = {}
        for u in all_users:
            users[u[0]] = u[1]

        all_messages = list(select((msg.tg_user_id, count()) for msg in Message).order_by(lambda: desc(count())))
        number = len(all_messages)
        try:
            number = abs(int(args[0]))
        except:
            pass
        rank_text = ""
        c = 1
        for r in all_messages[:number]:
            rank_text += "*{}. {}* => {}\n".format(c, users[r[0]], r[1])
            c += 1
        return rank_text
