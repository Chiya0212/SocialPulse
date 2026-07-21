from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('edit/', views.ProfileEditView.as_view(), name='edit'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('theme/', views.ThemeToggleView.as_view(), name='theme'),
    path('u/<str:username>/', views.ProfileDetailView.as_view(), name='profile'),
]
