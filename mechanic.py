#!/usr/bin/env python
from RabbitFrame import RabbitFrame


class Mechanic(RabbitFrame):

    def __init__(self):
        super(Mechanic, self).__init__()
        self.channel.exchange_declare(exchange='error', exchange_type='direct')
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue

    def call(self):
        severity = 'error'
        self.channel.queue_bind(
            exchange='error', queue=self.queue_name, routing_key=severity)
        print(' [*] Waiting for info from monitoring. To exit press CTRL+C')
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))
