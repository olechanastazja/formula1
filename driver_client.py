#!/usr/bin/env python
import pika
import uuid
from RabbitFrame import RabbitFrame


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

    def ask(self, message):
        print(message)
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
        print(self.response)
        return self.response

    def receive_warnings(self):
        severity = 'warning'
        self.receive_channel.queue_bind(
            exchange='warning', queue=self.queue_name, routing_key=severity)

        print(' [*] Waiting for monitoring info. To exit press CTRL+C')

        self.receive_channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)

        self.receive_channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))
