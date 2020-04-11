#!/usr/bin/env python
import pika
import sys


class Bolid:

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='logging', exchange_type='fanout')

    def call(self):
        message = ' '.join(sys.argv[1:])
        self.channel.basic_publish(exchange='logging', routing_key='', body=message)
        print(" [x] Sent %r" % message)
        self.connection.close()
