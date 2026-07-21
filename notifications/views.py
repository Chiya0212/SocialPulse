from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.http import JsonResponse
from django.shortcuts import redirect
from .models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    template_name = 'notifications/list.html'
    context_object_name = 'notifications'
    paginate_by = 30

    def get_queryset(self):
        qs = self.request.user.notifications.select_related('actor')
        qs.filter(is_read=False).update(is_read=True)
        return qs


class MarkReadView(LoginRequiredMixin, View):
    def post(self, request):
        request.user.notifications.update(is_read=True)
        return JsonResponse({'ok': True})
