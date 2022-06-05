from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets

from posts.models import Post, Group, Follow, User
from .permissions import UserOrReadOnly, ReadOnly
from .serializers import PostSerializer, CommentSerializer, GroupSerializer, \
    FollowSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (UserOrReadOnly,)

    def get_permissions(self):
        if self.action == 'retrieve':
            return ReadOnly(),
        return super().get_permissions()

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (UserOrReadOnly,)

    def get_permissions(self):
        if self.action == 'retrieve':
            return ReadOnly(),
        return super().get_permissions()

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return serializer.save(post=post, author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=following__username',)

    def get_queryset(self):
        following = Follow.objects.filter(user=self.request.user)
        return following

    def perform_create(self, serializer):
        user = self.request.user
        following = get_object_or_404(
            User, username=self.request.data['following']
        )
        return serializer.save(user=user, following=following)
