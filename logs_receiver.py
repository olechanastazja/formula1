from RabbitFrame import RabbitFrame


class LogsReceiver(RabbitFrame):

    def __init__(self):
        super(LogsReceiver, self).__init__()
        self.channel.exchange_declare(exchange='logging', exchange_type='fanout')
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange='logging', queue=self.queue_name)

    def call(self):
        print(' [*] Waiting for logs. To exit press CTRL+C')
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    @staticmethod
    def callback(ch, method, properties, body):
        print("Logs %r" % body)
        with open('logs.txt', 'a') as file:
            file.write(str(body) + '\n')



