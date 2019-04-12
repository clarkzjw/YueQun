import os

import pika

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "123456789:A-AHYaxhIoUIAPXdbFtD0YD4Jk9qB18VnPo")
TG_IN_USE_GROUP = os.getenv("TG_IN_USE_GROUP", "-215701199")
# should be different with TG_BOT_TOKEN
TG_KEYWORD_BOT_TOKEN = os.getenv("TG_KEYWORD_BOT_TOKEN", "123456789:A-AHYaxhIoUIAPXdbFtD0YD4Jk9qB18VnPo")


MQ_ADDRESS = os.getenv("MQ_ADDRESS", "127.0.0.1")
MQ_PORT = os.getenv("MQ_PORT", 5672)
MQ_CHANNEL_GROUP_MESSAGE = "group_message"
MQ_CHANNEL_BOT_CMD = "bot_command"
MQ_USERNAME = os.getenv("MQ_USERNAME", "guest")
MQ_PASSWORD = os.getenv("MQ_PASSWORD", "guest")

credentials = pika.PlainCredentials(MQ_USERNAME, MQ_PASSWORD)
MQ_PARAMS = pika.ConnectionParameters(MQ_ADDRESS, int(MQ_PORT), '/', credentials)


MYSQL_ADDRESS = os.getenv("MYSQL_ADDRESS", "127.0.0.1")
MYSQL_PORT = os.getenv("MYSQL_PORT", 3306)
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASS = os.getenv("MYSQL_PASS", "root")
MYSQL_DB = os.getenv("MYSQL_DB", "yuequnbot")

INFLUXDB_ADDRESS = os.getenv("INFLUXDB_ADDRESS", "127.0.0.1")
INFLUXDB_PORT = os.getenv("INFLUXDB_PORT", "8086")
INFLUXDB_USERNAME = os.getenv("INFLUXDB_USERNAME", "test")
INFLUXDB_PASSWORD = os.getenv("INFLUXDB_PASSWORD", "test")
INFLUXDB_DBNAME = os.getenv("INFLUXDB_DBNAME", "yuequn")

