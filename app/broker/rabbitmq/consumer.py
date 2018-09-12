#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

channel.queue_declare(queue='raw_update')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % json.loads(body))


channel.basic_consume(callback,
                      queue='raw_update',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
