#!/usr/bin/env python
import pika
from random import choice
import RabbitFrame


class Director(RabbitFrame):

    def __init__(self):
        self.channel.queue_declare(queue='rpc_queue')

    @staticmethod
    def yes_or_no():
        answer = choice(['yes', 'no'])
        return answer

    def on_request(self, ch, method, props, body):
        print(body)
        response = self.yes_or_no()

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                             props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def call(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='rpc_queue', on_message_callback=self.on_request)
        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()


director = Director()
director.call()
