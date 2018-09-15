from config.common import TG_IN_USE_GROUP
from model.db import User, db_session, commit, Message
from pony.orm.core import select



def get_rank():
    with db_session:
        all_messages = select(msg for msg in Message)
        all_users = [msg.tg_user_username for msg in all_messages]
        rank = {u: all_users.count(u) for u in all_users}
        rank = sorted(rank.items(), key=lambda x: x[1], reverse=True)
        rank_text = ""
        for r in rank:
            rank_text += "*{}* => {}\n".format(r[0], r[1])
        return rank_text
