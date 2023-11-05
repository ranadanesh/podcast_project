import json
import pika


def publish(queue, body):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('amqp://guest:guest@rabbitmq:5672/%2F'))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(body))
    connection.close()


