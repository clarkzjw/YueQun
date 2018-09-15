from pony.orm import *
from config.common import MYSQL_ADDRESS, MYSQL_PORT,MYSQL_USER, MYSQL_PASS, MYSQL_DB
from datetime import datetime

db = Database()
db.bind(provider='mysql', host=MYSQL_ADDRESS, user=MYSQL_USER, passwd=MYSQL_PASS, db=MYSQL_DB, charset='utf8mb4')


def init_db():
    print("Initializing Database……")
    db.generate_mapping(create_tables=True)


class Message(db.Entity):
    id = PrimaryKey(int, auto=True)
    tg_user_id = Required(int, size=64)
    tg_user_username = Optional(str)

    tg_msg_id = Required(int, size=64)
    tg_msg_text = Required(str)
    tg_msg_is_reply = Optional(bool, default=False)
    tg_msg_is_mention = Optional(bool, default=False)
    tg_msg_timestamp = Required(datetime)

    tg_msg_is_sticker = Optional(bool, default=0)

    tg_update_id = Required(int, size=64)
    tg_update_full = Required(bytes)


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    tg_user_id = Required(int, size=64)
    tg_user_username = Optional(str)
    tg_user_nickname = Optional(str)
    tg_user_ignore = Optional(bool, default=False)


class HourlyReport(db.Entity):
    id = PrimaryKey(int, auto=True)
    hour_id = Optional(int, size=8)  # 当天的小时id，取值1-12
    metadata = Optional(bytes)
    daily_report_id = Optional(int, size=16)


class DailyReport(db.Entity):
    id = PrimaryKey(int, auto=True)
    metadata = Optional(bytes)
    weekly_report_id = Optional(int, size=16)


class WeeklyReport(db.Entity):
    id = PrimaryKey(int, auto=True)
    metadata = Optional(bytes)
    monthly_report_id = Optional(int, size=16)


class MonthlyReport(db.Entity):
    id = PrimaryKey(int, auto=True)
    metadata = Optional(bytes)
    yearly_report_id = Optional(int, size=16)


class YearlyReport(db.Entity):
    id = PrimaryKey(int, auto=True)
    metadata = Optional(bytes)


class Reminder(db.Entity):
    id = PrimaryKey(int, auto=True)
    keyword = Required(str)
    tg_user_id = Required(int, size=64)


class BotCommand(db.Entity):
    id = PrimaryKey(int, auto=True)
    tg_user_id = Required(int, size=64)
    tg_cmd_timestamp = Required(datetime)
    tg_cmd_text = Required(str)
    tg_update_id = Required(int, size=64)
    tg_update_full = Required(bytes)
