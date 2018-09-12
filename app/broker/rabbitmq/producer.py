import json
import pickle


def send_raw_update_to_mq(chan, update):
    chan.queue_declare(queue='raw_update')
    chan.basic_publish(exchange="",
                       routing_key="raw_update",
                       body=pickle.dumps(update))
