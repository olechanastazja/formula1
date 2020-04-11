#!/usr/bin/env python
import sys
import RabbitFrame


class Bolid(RabbitFrame):

    def __init__(self):
        super(Bolid, self).__init__()
        self.channel.exchange_declare(exchange='logging', exchange_type='fanout')

    def call(self):
        message = ' '.join(sys.argv[1:])
        self.channel.basic_publish(exchange='logging', routing_key='', body=message)
        print(" [x] Sent %r" % message)
        self.connection.close()


bolid = Bolid()
bolid.call()
