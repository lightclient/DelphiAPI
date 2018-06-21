import pika
import time
import os

url = ''
if os.environ.get('RABBITMQ_BIGWIG_URL'):
    url = os.environ.get('RABBITMQ_BIGWIG_URL')
else:
    url = 'amqp://guest:guest@localhost:5672'

parameters = pika.URLParameters(url)
connection = pika.BlockingConnection(parameters)
client = connection.channel()
client.queue_declare(queue='delphi_events', durable=True)
client.basic_qos(prefetch_count=1)
