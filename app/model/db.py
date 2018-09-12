from pony.orm import *


db = Database()


class Message(db.Entity):
    id = PrimaryKey(int, auto=True)
    tg_user_id = Required(int, size=64)
    tg_msg_id = Required(int, size=64)
    tg_msg_text = Required(str)
    tg_msg_url = Optional(str)
    tg_msg_is_reply = Optional(bool, default=False)
    tg_msg_is_at = Optional(bool, default=False)
    tg_msg_timestamp = Required(int, size=64)
    tg_update_id = Required(int, size=64)
    tg_update_full = Required(Json)


class User(db.Entity):
    id = Required(int)
    tg_user_id = Required(int, size=64)
    tg_user_username = Optional(str)
    tg_user_nickname = Optional(str)
    tg_user_ignore = Optional(bool, default=False)
    PrimaryKey(id, tg_user_id)


class HourlyReport(db.Entity):
    id = PrimaryKey(int, auto=True)
    hour_id = Optional(int, size=8)  # 当天的小时id，取值1-12
    metadata = Optional(Json)
    daily_report_id = Optional(int, size=16)


class DailyReport(db.Entity):
    id = PrimaryKey(int, auto=True)
    metadata = Optional(Json)
    weekly_report_id = Optional(int, size=16)


class WeeklyReport(db.Entity):
    id = PrimaryKey(int, auto=True)
    metadata = Optional(Json)
    monthly_report_id = Optional(int, size=16)


class MonthlyReport(db.Entity):
    id = PrimaryKey(int, auto=True)
    metadata = Optional(Json)
    yearly_report_id = Optional(int, size=16)


class YearlyReport(db.Entity):
    id = PrimaryKey(int, auto=True)
    metadata = Optional(Json)


class Reminder(db.Entity):
    id = PrimaryKey(int, auto=True)
    keyword = Required(str)
    tg_user_id = Required(int, size=64)


db.generate_mapping()
