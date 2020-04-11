#!/usr/bin/env python
import pika
import uuid
import RabbitFrame


class DriverClient(RabbitFrame):

    def __init__(self):
        super(DriverClient, self).__init__()
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


driver_client = DriverClient()
print(" [x] Requesting reply form director")
response = driver_client.call('Czy moge zjechac do pit stopu Panie kierowniku?')
print(" [.] Got %r" % response)
