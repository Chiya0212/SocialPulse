from django.conf import settings
from django.db import models
from better_profanity import profanity

profanity.load_censor_words()


class Post(models.Model):
    PRIVACY = [('public', 'Public'), ('followers', 'Followers'), ('private', 'Only Me')]
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=2000)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY, default='public')
    is_flagged = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if profanity.contains_profanity(self.content):
            self.is_flagged = True
            self.content = profanity.censor(self.content)
        super().save(*args, **kwargs)

    def likes_count(self):
        return self.likes.count()

    def comments_count(self):
        return self.comments.count()

    def __str__(self):
        return f'{self.author.username}: {self.content[:30]}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if profanity.contains_profanity(self.text):
            self.text = profanity.censor(self.text)
        super().save(*args, **kwargs)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')
