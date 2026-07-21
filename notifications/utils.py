from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification


def push_notification(recipient, actor, kind, text, url=''):
    n = Notification.objects.create(recipient=recipient, actor=actor, kind=kind, text=text, url=url)
    try:
        layer = get_channel_layer()
        if layer:
            async_to_sync(layer.group_send)(f'user_{recipient.id}', {
                'type': 'notify',
                'payload': {
                    'id': n.id, 'kind': kind, 'text': text, 'url': url,
                    'actor': actor.username if actor else 'system',
                    'created_at': n.created_at.isoformat(),
                },
            })
    except Exception:
        pass
    return n
