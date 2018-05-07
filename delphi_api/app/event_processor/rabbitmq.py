import pika
import time

parameters = pika.URLParameters('amqp://rabbitmq:rabbitmq@rabbitmq:5672')
connection = pika.BlockingConnection(parameters)
client = connection.channel()
client.queue_declare(queue='delphi_events', durable=True)
client.basic_qos(prefetch_count=1)
