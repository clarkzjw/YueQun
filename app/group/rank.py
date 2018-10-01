from pony.orm.core import select, count, desc

from model.db import db_session, Message, User


def get_rank(args):
    with db_session:
        all_users = list(select((user.tg_user_id, user.tg_user_username) for user in User))
        users = {}
        for u in all_users:
            users[u[0]] = u[1]

        all_messages = list(select((msg.tg_user_id, count()) for msg in Message).order_by(lambda: desc(count())))
        try:
            number = abs(int(args[0]))  # 如果输入负数，展示绝对值对应的排名
        except:
            number = 10  # 默认展示前10名，如果参数不是数字也只显示前10名
        if number == 0:  # 输入数字0展示全部排名
            number = len(all_messages)
        rank_text = ""
        c = 1
        for r in all_messages[:number]:
            rank_text += "*{}. {}* => {}\n".format(c, users[r[0]], r[1])
            c += 1
        return rank_text
