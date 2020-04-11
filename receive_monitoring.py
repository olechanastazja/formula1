#!/usr/bin/env python
import pika
import sys

# nawiązujemy połącznie
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# deklaruje exchange z nazwą logging, typ fanout (wysyłą wiadomości do wszystkich kolejek jakie zna)
channel.exchange_declare(exchange='monitoring', exchange_type='fanout')

# randomowa nazwa kolejki, zostanie usunięta po zakończeniu
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# bindowanie exchange z kolejką
channel.queue_bind(exchange='logging', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    if len(body) > 50:
        channel.exchange_declare(exchange='error', exchange_type='direct')
        severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
        message = ' '.join(sys.argv[2:]) or 'Hello World!'
        channel.basic_publish(
            exchange='error', routing_key=severity, body=message)
        print(" [x] Sent %r:%r" % (severity, message))
        connection.close()
    elif len(body) > 20:
        channel.exchange_declare(exchange='warning', exchange_type='direct')
        severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
        message = ' '.join(sys.argv[2:]) or 'Hello World!'
        channel.basic_publish(
            exchange='warning', routing_key=severity, body=message)
        print(" [x] Sent %r:%r" % (severity, message))
        connection.close()
    print(" [x] %r" % body)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
