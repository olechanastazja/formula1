#!/usr/bin/env python
import pika

# nawiązujemy połącznie
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# deklaruje exchange z nazwą logging, typ fanout (wysyłą wiadomości do wszystkich kolejek jakie zna)
channel.exchange_declare(exchange='logging', exchange_type='fanout')

# randomowa nazwa kolejki, zostanie usunięta po zakończeniu
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# bindowanie exchange z kolejką
channel.queue_bind(exchange='logging', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r" % body)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
