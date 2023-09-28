from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from .serializers import UserSerializer, LikesSerializer, CommentSerializer
from rest_framework.response import Response
from .models import CustomUser, Likes, Comment
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
# Create your views here.


class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User Not Found Error!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password Error!')

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()  # the day which this token is created
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}

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

    def get(self, request):
        user = request.user
        episode_id = request.data.get('episode_id')
        like = Likes.objects.get(user=user, episode=episode_id)
        if like:
            like.delete()
            return Response({'detail': 'Unliked'}, status=status.HTTP_204_NO_CONTENT)
        if not like:
            user = user.id
            Likes.objects.create(user, episode_id)
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
