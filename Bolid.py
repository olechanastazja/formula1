import json
from datetime import datetime
from RabbitFrame import RabbitFrame


class Bolid(RabbitFrame):

    def __init__(self, engine_temperature, tire_pressure, oil_pressure):
        super(Bolid, self).__init__()
        self.engine_temperature = engine_temperature
        self.tire_pressure = tire_pressure
        self.oil_pressure = oil_pressure
        self.channel.exchange_declare(exchange='logging', exchange_type='fanout')

    def call(self):
        message_body = {
            'engine_temperature': self.engine_temperature,
            'tire_pressure': self.tire_pressure,
            'oil_pressure': self.oil_pressure,
            'time': str(datetime.now())
        }
        message = json.dumps(message_body)
        self.channel.basic_publish(exchange='logging', routing_key='', body=message)
        print(" [x] Sent %r" % message)
        self.connection.close()
