# #!/usr/bin/env python
# import pika

# connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
# channel = connection.channel()
#
#
# channel.queue_declare(queue='hello')
#
# channel.basic_publish(exchange='',
#                       routing_key='hello',
#                       body='Hello World2!')
# print(" [x] Sent 'Hello World!'")

import json

def send_raw_update_to_mq(chan, update):
    chan.queue_declare(queue='raw_update')
    chan.basic_publish(exchange="",
                       routing_key="raw_update",
                       body=json.dumps(str(update)))
