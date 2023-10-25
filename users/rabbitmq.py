import json
import pika


# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
# channel = connection.channel()

#
# def publish(queue, method, body):
#     properties = pika.BasicProperties(method)
#     channel = connection.channel()
#     channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(body), properties=properties)
#     return channel


def publish(queue, body):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(body))
    connection.close()




# import json
# import pika
#
#
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
# channel = connection.channel()
# def rabbitmq_client(method, body):
#     properties = pika.BasicProperties(method)
#     channel.basic_publish(exchange='', routing_key='likes', body=json.dumps(body), properties=properties)