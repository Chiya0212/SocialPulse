from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='home'),
    path('stats/', views.DashboardStatsView.as_view(), name='stats'),
    path('users/', views.UserManageListView.as_view(), name='users'),
    path('users/<int:pk>/staff/', views.UserToggleStaffView.as_view(), name='user_staff'),
    path('users/<int:pk>/active/', views.UserToggleActiveView.as_view(), name='user_active'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('posts/', views.PostManageListView.as_view(), name='posts'),
    path('posts/<int:pk>/hide/', views.PostToggleHiddenView.as_view(), name='post_hide'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('comments/', views.CommentManageListView.as_view(), name='comments'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('broadcast/', views.BroadcastView.as_view(), name='broadcast'),
]
