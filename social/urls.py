from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('follow/<str:username>/', views.FollowToggleView.as_view(), name='follow'),
    path('friend/<str:username>/', views.FriendRequestSendView.as_view(), name='friend_send'),
    path('friend/respond/<int:pk>/', views.FriendRequestRespondView.as_view(), name='friend_respond'),
    path('requests/', views.FriendRequestsListView.as_view(), name='requests'),
    path('followers/<str:username>/', views.FollowersListView.as_view(), name='followers'),
    path('following/<str:username>/', views.FollowingListView.as_view(), name='following'),
]
