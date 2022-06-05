from django.urls import path, include
from rest_framework import routers

from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet

app_name = 'api'

routers = routers.DefaultRouter()
routers.register('posts', PostViewSet, basename='posts')
routers.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments')
routers.register('groups', GroupViewSet, basename='groups')
routers.register('follow', FollowViewSet, basename='follows')


urlpatterns = [
    path('v1/', include(routers.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
