#!/usr/bin/env python
import pickle

import pika
from pony.orm import db_session, commit

from config.common import MQ_ADDRESS, MQ_CHANNEL_GROUP_MESSAGE
from model.db import Message, db

connection = pika.BlockingConnection(pika.ConnectionParameters(MQ_ADDRESS))
channel = connection.channel()

channel.queue_declare(queue=MQ_CHANNEL_GROUP_MESSAGE)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % pickle.loads(body))
    update = pickle.loads(body)
    with db_session:
        Message(tg_user_id=update.message.from_user.id,
                tg_msg_id=update.message.message_id,
                tg_msg_text=update.message.text,
                tg_msg_timestamp=update.message.date,
                tg_update_id=update.update_id,
                tg_update_full=body)
        commit()


channel.basic_consume(callback,
                      queue=MQ_CHANNEL_GROUP_MESSAGE,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
db.generate_mapping()
channel.start_consuming()
