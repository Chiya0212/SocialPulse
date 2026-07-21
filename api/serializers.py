from rest_framework import serializers
from django.contrib.auth import get_user_model
from posts.models import Post, Comment, Like
from social.models import Follow, FriendRequest
from notifications.models import Notification

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.CharField(read_only=True)
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'bio', 'avatar_url',
                  'location', 'website', 'is_private', 'followers_count', 'following_count')


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'created_at')
        read_only_fields = ('author',)


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'image', 'video', 'privacy',
                  'likes_count', 'comments_count', 'created_at')
        read_only_fields = ('author',)


class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = ('id', 'kind', 'text', 'url', 'actor', 'is_read', 'created_at')
