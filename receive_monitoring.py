#!/usr/bin/env python
import pika
import sys
import RabbitFrame


class Monitoring(RabbitFrame):

    def __init__(self):
        super(Monitoring, self).__init__()
        self.channel.exchange_declare(exchange='monitoring', exchange_type='fanout')
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange='logging', queue=self.queue_name)

    def call(self):
        print(' [*] Waiting for logs. To exit press CTRL+C')
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        if len(body) > 50:
            self.channel.exchange_declare(exchange='error', exchange_type='direct')
            severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
            message = ' '.join(sys.argv[2:]) or 'Hello World!'
            self.channel.basic_publish(
                exchange='error', routing_key=severity, body=message)
            print(" [x] Sent %r:%r" % (severity, message))
        elif len(body) > 20:
            self.channel.exchange_declare(exchange='warning', exchange_type='direct')
            severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
            message = ' '.join(sys.argv[2:]) or 'Hello World!'
            self.channel.basic_publish(
                exchange='warning', routing_key=severity, body=message)
            print(" [x] Sent %r:%r" % (severity, message))
        self.connection.close()
        print(" [x] %r" % body)


monitoring = Monitoring()
monitoring.call()
