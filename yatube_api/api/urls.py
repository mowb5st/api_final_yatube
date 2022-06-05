from rest_framework import routers
from django.urls import path, include
from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet


app_name = 'api'

routers = routers.DefaultRouter()
routers.register('posts', PostViewSet, basename='posts')
routers.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment')
routers.register('groups', GroupViewSet, basename='groups')
routers.register('follow', FollowViewSet, basename='follow')


urlpatterns = [
    path('', include(routers.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
