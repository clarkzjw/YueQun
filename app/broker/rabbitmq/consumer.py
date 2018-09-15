#!/usr/bin/env python
import logging
import pickle

import pika
from pony.orm import db_session, commit

from config.common import MQ_ADDRESS, MQ_CHANNEL_GROUP_MESSAGE
from group.common import insert_user_by_update
from group.parse import check_is_mention, check_is_reply, check_is_sticker, check_user_ignore
from model.db import Message, db

connection = pika.BlockingConnection(pika.ConnectionParameters(MQ_ADDRESS))
channel = connection.channel()

channel.queue_declare(queue=MQ_CHANNEL_GROUP_MESSAGE)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    update = pickle.loads(body)
    logger.info(update)

    if check_user_ignore(update):
        pass
    else:
        try:
            with db_session:
                Message(tg_user_id=update.message.from_user.id,
                        tg_user_username=update.message.from_user.username,
                        tg_msg_id=update.message.message_id,
                        tg_msg_text=update.message.text if not check_is_sticker(update) else update.message.sticker.emoji,
                        tg_msg_timestamp=update.message.date,
                        tg_update_id=update.update_id,
                        tg_msg_is_reply=check_is_reply(update),
                        tg_msg_is_mention=check_is_mention(update),
                        tg_msg_is_sticker=check_is_sticker(update),
                        tg_update_full=body)
                insert_user_by_update(update)
                commit()
        except ValueError:
            pass


channel.basic_consume(callback,
                      queue=MQ_CHANNEL_GROUP_MESSAGE,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
db.generate_mapping()
channel.start_consuming()
