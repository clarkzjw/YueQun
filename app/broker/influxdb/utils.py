from influxdb import InfluxDBClient
from config.common import INFLUXDB_ADDRESS, INFLUXDB_DBNAME, INFLUXDB_PASSWORD, INFLUXDB_PORT, INFLUXDB_USERNAME
from group.parse import check_is_sticker, check_is_mention, check_is_reply, check_user_ignore


def insert_update_to_influxdb(update):
    client = InfluxDBClient(INFLUXDB_ADDRESS, INFLUXDB_PORT, INFLUXDB_USERNAME, INFLUXDB_PASSWORD, INFLUXDB_DBNAME)
    influx_msg = [
        {
            "measurement": "message",
            "time": update.message.date,
            "tags": {
                "group": "hzres",
            },
            "fields": {
                "tg_user_id": update.message.from_user.id,
                "tg_user_username": update.message.from_user.username,
                "tg_msg_id": update.message.message_id,
                "tg_msg_text": update.message.text if not check_is_sticker(
                                update) else update.message.sticker.emoji,
                "tg_update_id": update.update_id
            }
        }
    ]
    client.write_points(influx_msg)
