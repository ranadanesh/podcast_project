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


class CustomJwtAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'
    authentication_header_name = 'Authorization'

    @staticmethod
    def get_payload_from_refresh_token(refresh_token):
        try:
            payload = decode_jwt(refresh_token)
            return payload
        except jwt.ExpiredSignatureError:
            raise exceptions.PermissionDenied(
                'Expired refresh token, please login again.')
        except Exception as e:
            raise exceptions.NotAcceptable(str(e))

    @staticmethod
    def get_user_from_payload(payload):

        user_id = payload.get('id')
        if user_id is None:
            raise exceptions.NotFound("User Not Found Error")

        try:
            user = user_model.objects.get(id=user_id)
            return user
        except:
            raise exceptions.NotFound("User Not Found ERROR")

    def authenticate(self, request):

        access_token = request.headers.get('Authorization')

        payload = self.get_payload_from_refresh_token(access_token)
        user = self.get_user_from_payload(payload)

        return user, payload









