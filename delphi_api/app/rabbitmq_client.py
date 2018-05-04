import pika
from django.conf import settings

if settings.LOCAL:
    p = pika.URLParameters('amqp://rabbitmq:rabbitmq@rabbitmq:5672')
    connection = pika.BlockingConnection(p)
    rabbitmq_client = connection.channel()
else:
    raise Exception('no production configuration for rabbitmq set up yet')
