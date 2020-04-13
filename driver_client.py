#!/usr/bin/env python
import pika
import uuid
import RabbitFrame
import sys


class DriverClient(RabbitFrame):

    def __init__(self):
        super(DriverClient, self).__init__()
        self.receive_channel = self.connection.channel()
        self.receive_channel.exchange_declare(exchange='warning', exchange_type='direct')
        receive_result = self.receive_channel.queue_declare(queue='', exclusive=True)
        self.queue_name = receive_result.method.queue
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)
        self.response = None
        self.corr_id = str(uuid.uuid4())

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, message):
        self.receive_warnings()
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=message)
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def receive_warnings(self):
        severities = sys.argv[1:]
        if not severities:
            sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
            sys.exit(1)

        for severity in severities:
            self.receive_channel.queue_bind(
                exchange='warning', queue=self.queue_name, routing_key=severity)

        print(' [*] Waiting for logs. To exit press CTRL+C')

        self.receive_channel.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)

        self.receive_channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))


driver_client = DriverClient()
print(" [x] Requesting reply form director")
response = driver_client.call('Czy moge zjechac do pit stopu Panie kierowniku?')
print(" [.] Got %r" % response)
