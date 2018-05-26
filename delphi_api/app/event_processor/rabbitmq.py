import pika
import time
import os

url = ''
if os.environ['ENV'] == 'DEV':
    url = 'amqp://%s:%s@%s:%s' % (
        os.environ['RABBITMQ_DEFAULT_USER'],
        os.environ['RABBITMQ_DEFAULT_PASS'],
        os.environ['RABBITMQ_HOST'],
        os.environ['RABBITMQ_PORT']
    )
else:
    url = os.environ['RABBITMQ_BIGWIG_URL']

parameters = pika.URLParameters(url)
connection = pika.BlockingConnection(parameters)
client = connection.channel()
client.queue_declare(queue='delphi_events', durable=True)
client.basic_qos(prefetch_count=1)
