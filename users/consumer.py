import json

import pika

from .models import Notification, CustomUser


def login_callback(ch, method, properties, body):
    data = json.loads(body)
    user = CustomUser.objects.get(data['email'])
    # print("1"*100)
    Notification.objects.create(message=body['message'], user=user)


def login_consume():
    connection = pika.BlockingConnection(
        pika.URLParameters('amqp://guest:guest@rabbitmq:5672'))
    channel = connection.channel()

    channel.queue_declare(queue='login')
    channel.basic_consume(queue='login', on_message_callback=login_callback)

    print('Consuming...')
    channel.start_consuming()


def register_callback(ch, method, properties, body):
    data = json.loads(body)
    user = CustomUser.objects.get(data['email'])
    Notification.objects.create(message=body['message'], user=user)


def register_consume():
    connection = pika.BlockingConnection(
        pika.URLParameters('amqp://guest:guest@rabbitmq:5672'))
    channel = connection.channel()

    channel.queue_declare(queue='register')
    channel.basic_consume(queue='register', on_message_callback=login_callback)

    channel.start_consuming()
