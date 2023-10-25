from rest_framework import serializers
from .models import CustomUser, Likes, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['episode_id']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['episode', 'text']
