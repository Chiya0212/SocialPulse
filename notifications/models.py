from django.conf import settings
from django.db import models


class Notification(models.Model):
    KINDS = [('like', 'Like'), ('comment', 'Comment'), ('follow', 'Follow'),
             ('friend_request', 'Friend Request'), ('friend_accept', 'Friend Accept'),
             ('mention', 'Mention'), ('system', 'System')]
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    kind = models.CharField(max_length=20, choices=KINDS)
    text = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
