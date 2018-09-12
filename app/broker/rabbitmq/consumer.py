#!/usr/bin/env python
import pika
import json
from pony.orm import db_session,commit
from model.db import Message, db
import pickle

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

channel.queue_declare(queue='raw_update')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % pickle.loads(body))
    update = pickle.loads(body)
    with db_session:
        Message(tg_user_id=update.message.from_user.id,
                tg_msg_id=update._effective_message.message_id,
                tg_msg_text=update._effective_message.text,
                tg_msg_timestamp=update._effective_message.date,
                tg_update_id=update.update_id,
                tg_update_full=body)
        commit()


channel.basic_consume(callback,
                      queue='raw_update',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
db.generate_mapping()
channel.start_consuming()
