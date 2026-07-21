from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    birth_date = models.DateField(blank=True, null=True)
    is_private = models.BooleanField(default=False)
    theme = models.CharField(max_length=10, default='dark',
                             choices=[('light', 'Light'), ('dark', 'Dark'), ('dusk', 'Dusk')])
    created_at = models.DateTimeField(auto_now_add=True)

    def followers_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()

    def posts_count(self):
        return self.posts.count()

    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return f'https://api.dicebear.com/7.x/identicon/svg?seed={self.username}'

    def __str__(self):
        return self.username
