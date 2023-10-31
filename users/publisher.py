import json
import pika


def publish(queue, body):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(body))
    connection.close()


