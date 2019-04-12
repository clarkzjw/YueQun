from influxdb import InfluxDBClient
from model.db import db_session, select, Message, db
from config.common import INFLUXDB_ADDRESS, INFLUXDB_DBNAME, INFLUXDB_PASSWORD, INFLUXDB_PORT, INFLUXDB_USERNAME


def migrate():
    client = InfluxDBClient(INFLUXDB_ADDRESS, INFLUXDB_PORT, INFLUXDB_USERNAME, INFLUXDB_PASSWORD, INFLUXDB_DBNAME)
    with db_session:
        all_messages = list(select(m for m in Message))
        count = 1
        for msg in all_messages:
            print(count)
            count += 1
            influx_msg = [
                {
                    "measurement": "message",
                    "time": msg.tg_msg_timestamp,
                    "tags": {
                        "group": "hzres",
                    },
                    "fields": {
                        "tg_user_id": msg.tg_user_id,
                        "tg_user_username": msg.tg_user_username,
                        "tg_msg_id": msg.tg_msg_id,
                        "tg_msg_text": msg.tg_msg_text,
                        "tg_msg_is_reply": msg.tg_msg_is_reply,
                        "tg_msg_is_mention": msg.tg_msg_is_mention,
                        "tg_msg_is_sticker": msg.tg_msg_is_sticker,
                        "tg_update_id": msg.tg_update_id
                    }
                }
            ]
            client.write_points(influx_msg)


if __name__ == "__main__":
    db.generate_mapping(create_tables=True)
    migrate()