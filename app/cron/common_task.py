from model.db import db_session, select, count, Message, db, User
import datetime


def count_daily_stats():
    with db_session:
        total = count(m for m in Message if m.tg_msg_timestamp >= datetime.date(2019, 3, 19))
        print(total)



def count_recent_30_days_stats():
    today = datetime.datetime.today().date()
    this_month = [today - datetime.timedelta(days=i) for i in range(0, 30)]
    for i in range(1, 30):
        with db_session:
            total = count(m for m in Message if m.tg_msg_timestamp >= this_month[i]
                          and m.tg_msg_timestamp < this_month[i-1])
            print(this_month[i], total)


if __name__ == "__main__":
    db.generate_mapping()
    # count_daily_stats()
    # count_daily_stats(123)
    # today = datetime.datetime.today().date()
    # yesterday = today - datetime.timedelta(days=1)
    count_recent_30_days_stats()
