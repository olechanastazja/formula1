#!/usr/bin/env python
import pika
import sys
import RabbitFrame


class Mechanic(RabbitFrame):

    def __init__(self):
        super(Mechanic, self).__init__()
        self.channel.exchange_declare(exchange='error', exchange_type='direct')
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue

    def call(self):
        severities = sys.argv[1:]

        if not severities:
            sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
            sys.exit(1)

        for severity in severities:
            self.channel.queue_bind(
                exchange='error', queue=self.queue_name, routing_key=severity)

        print(' [*] Waiting for logs. To exit press CTRL+C')

        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)

        self.channel.start_consuming()

    def callback(self,ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))


mechanic = Mechanic()
mechanic.call()
