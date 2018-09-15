import os

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "123456789:A-AHYaxhIoUIAPXdbFtD0YD4Jk9qB18VnPo")
TG_IN_USE_GROUP = os.getenv("TG_IN_USE_GROUP", "-215701199")


MQ_ADDRESS = os.getenv("MQ_ADDRESS", "127.0.0.1")
MQ_PORT = os.getenv("MQ_PORT", "5672")
MQ_CHANNEL_GROUP_MESSAGE = "group_message"
MQ_CHANNEL_BOT_CMD = "bot_command"


MYSQL_ADDRESS = os.getenv("MYSQL_ADDRESS", "127.0.0.1")
MYSQL_PORT = os.getenv("MYSQL_PORT", 3306)
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASS = os.getenv("MYSQL_PASS", "root")
MYSQL_DB = os.getenv("MYSQL_DB", "yuequnbot")

