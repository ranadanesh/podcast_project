from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from .serializers import UserSerializer, LikesSerializer, CommentSerializer
from .authentication import CustomAuthBackend, CustomJwtAuthentication
from rest_framework.response import Response
from .models import CustomUser, Likes, Comment
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
from django.core.cache import caches
from uuid import uuid4
from podcast.models import Episode
# from .rabbitmq import publish
from .rabbitmq import publish
# Create your views here.





class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)
        body = {"message": f"user {user.id} registered"}
        publish('registered', body)
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        username = email.split('@')[0]

        user = CustomAuthBackend().authenticate(request=request, email=email, password=password)
        queue = 'user logged in'
        body = {"message": f"user {user.id} logged in"}
        publish(queue, body)


        if user is None:
            raise AuthenticationFailed('User Not Found Error!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password Error!')

        jti = uuid4().hex

        access_payload = {
            "token_type": "access",
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            "iat": datetime.datetime.utcnow(),  # the day which this token is created
            "jti": jti
        }

        refresh_payload = {
            "token_type": "refresh",
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=10),
            "iat": datetime.datetime.utcnow(),  # the day which this token is created
            "jti": jti
        }

        access_token = jwt.encode(access_payload, 'secret', algorithm='HS256')
        refresh_token = jwt.encode(refresh_payload, 'secret', algorithm='HS256')
        caches['auth'].set(jti, user.id)

        response = Response()
        response.data = {'access_token': access_token, 'refresh_token': refresh_token}



        # response.set_cookie(key='jwt', value=access_token, httponly=True)
        # response.data = {'jwt': access_token}

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            return AuthenticationFailed('Not Authenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            return AuthenticationFailed('Not Authenticated!')

        user = CustomUser.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        """ what we have to do for logout is to just delete the cookie """

        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class LikesView(APIView):

    serializer_class = LikesSerializer
    permission_classes = [permissions.IsAuthenticated,]
    authentication_classes = [CustomJwtAuthentication]

    def post(self, request):
        user = request.user
        episode_id = request.data.get('episode_id')
        episode = Episode.objects.get(id=episode_id)
        like, created = Likes.objects.get_or_create(user=user, episode=episode)
        if not created:
            like.delete()
            return Response({'detail': 'Unliked'}, status=status.HTTP_204_NO_CONTENT)

        return Response({'detail': 'Liked'}, status=status.HTTP_200_OK)


class CommentListCreateView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        episode_id = self.kwargs['episode_id']
        return Comment.objects.filter(episode=episode_id)

    def perform_create(self, serializer):
        episode_id = self.kwargs['episode_id']
        serializer.save(episode_id=episode_id)
