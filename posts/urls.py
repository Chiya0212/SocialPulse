from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.FeedView.as_view(), name='feed'),
    path('post/new/', views.PostCreateView.as_view(), name='create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete'),
    path('post/<int:pk>/like/', views.LikeToggleView.as_view(), name='like'),
    path('post/<int:pk>/comment/', views.CommentCreateView.as_view(), name='comment'),
]
