#!/usr/bin/env python
import json
import ast
from RabbitFrame import RabbitFrame


class Monitoring(RabbitFrame):

    def __init__(self):
        super(Monitoring, self).__init__()
        self.channel.exchange_declare(exchange='monitoring', exchange_type='fanout')
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange='logging', queue=self.queue_name)

    def call(self):
        print(' [*] Waiting for information from bolid. To exit press CTRL+C')
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        message = body
        dict_p = json.loads(json.dumps(str(body)))
        a = json.loads(ast.literal_eval(dict_p))
        info = [value for key, value in a.items()]
        for value in info[0:-1]:
            value = int(value)
            # Warunek sprawdza czy to poważna awaria (> 75) czy tylko przekroczenie parametrów (> 50)
            if value > 75:
                severity = 'error'
                self.channel.exchange_declare(exchange='error', exchange_type='direct')
                self.channel.basic_publish(
                    exchange='error', routing_key=severity, body=message)
                print(" [x] Sent %r:%r" % (severity, message))
            elif value > 50:
                severity = 'warning'
                self.channel.exchange_declare(exchange='warning', exchange_type='direct')
                self.channel.basic_publish(
                    exchange='warning', routing_key=severity, body=message)
                print(" [x] Sent %r:%r" % (severity, message))
