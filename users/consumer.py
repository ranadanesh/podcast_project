import json

import pika

from .models import Notification, CustomUser


def login_callback(ch, method, properties, body):
    data = json.loads(body)
    user = CustomUser.objects.get(data['email'])
    Notification.objects.create(message=body['message'], user=user)


