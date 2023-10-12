from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import check_password
from rest_framework import exceptions
from rest_framework import authentication
import jwt

from django.conf import settings

user_model = get_user_model()


class CustomAuthBackend(ModelBackend):

    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            user = user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None


def decode_jwt(token):
    payload = jwt.decode(token, 'secret',  algorithms=['HS256'])

    return payload







