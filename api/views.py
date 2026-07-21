from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from posts.models import Post, Comment, Like
from social.models import Follow
from notifications.models import Notification
from .serializers import (UserSerializer, PostSerializer, CommentSerializer,
                          NotificationSerializer)

User = get_user_model()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, 'author', getattr(obj, 'user', None)) == request.user


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    search_fields = ('username', 'first_name', 'last_name')

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def follow(self, request, username=None):
        target = self.get_object()
        rel, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if not created:
            rel.delete()
        return Response({'following': created})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(is_hidden=False).select_related('author')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    search_fields = ('content', 'author__username')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
        return Response({'liked': created, 'count': post.likes.count()})

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()
        return Response(CommentSerializer(post.comments.all(), many=True).data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.notifications.all()
