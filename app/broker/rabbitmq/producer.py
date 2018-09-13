import pickle

from config.common import MQ_CHANNEL_GROUP_MESSAGE


def send_raw_update_to_mq(chan, update):
    chan.queue_declare(queue=MQ_CHANNEL_GROUP_MESSAGE)
    chan.basic_publish(exchange="",
                       routing_key=MQ_CHANNEL_GROUP_MESSAGE,
                       body=pickle.dumps(update))
