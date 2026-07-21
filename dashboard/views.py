from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import TemplateView, ListView, View, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from posts.models import Post, Comment, Like
from social.models import Follow, FriendRequest
from notifications.models import Notification

User = get_user_model()


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class DashboardHomeView(AdminRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'total_users': User.objects.count(),
            'total_posts': Post.objects.count(),
            'total_comments': Comment.objects.count(),
            'total_likes': Like.objects.count(),
            'flagged_posts': Post.objects.filter(is_flagged=True).count(),
            'new_users_week': User.objects.filter(date_joined__gte=timezone.now() - timedelta(days=7)).count(),
            'recent_posts': Post.objects.select_related('author').order_by('-created_at')[:8],
            'top_users': User.objects.annotate(p=Count('posts')).order_by('-p')[:5],
        })
        return ctx


class DashboardStatsView(AdminRequiredMixin, View):
    def get(self, request):
        today = timezone.now().date()
        labels, users, posts = [], [], []
        for i in range(13, -1, -1):
            day = today - timedelta(days=i)
            labels.append(day.strftime('%b %d'))
            users.append(User.objects.filter(date_joined__date=day).count())
            posts.append(Post.objects.filter(created_at__date=day).count())
        return JsonResponse({
            'labels': labels, 'users': users, 'posts': posts,
            'pie': {
                'public': Post.objects.filter(privacy='public').count(),
                'followers': Post.objects.filter(privacy='followers').count(),
                'private': Post.objects.filter(privacy='private').count(),
            }
        })


class UserManageListView(AdminRequiredMixin, ListView):
    template_name = 'dashboard/users.html'
    paginate_by = 25
    context_object_name = 'users'

    def get_queryset(self):
        qs = User.objects.all().order_by('-date_joined')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(username__icontains=q)
        return qs


class UserToggleStaffView(AdminRequiredMixin, View):
    def post(self, request, pk):
        u = User.objects.get(pk=pk)
        if u == request.user:
            return JsonResponse({'error': 'cannot toggle self'}, status=400)
        u.is_staff = not u.is_staff
        u.save(update_fields=['is_staff'])
        return JsonResponse({'is_staff': u.is_staff})


class UserToggleActiveView(AdminRequiredMixin, View):
    def post(self, request, pk):
        u = User.objects.get(pk=pk)
        if u == request.user:
            return JsonResponse({'error': 'cannot toggle self'}, status=400)
        u.is_active = not u.is_active
        u.save(update_fields=['is_active'])
        return JsonResponse({'is_active': u.is_active})


class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('dashboard:users')
    template_name = 'dashboard/confirm_delete.html'


class PostManageListView(AdminRequiredMixin, ListView):
    template_name = 'dashboard/posts.html'
    paginate_by = 25
    context_object_name = 'posts'

    def get_queryset(self):
        qs = Post.objects.select_related('author').order_by('-created_at')
        f = self.request.GET.get('filter')
        if f == 'flagged':
            qs = qs.filter(is_flagged=True)
        elif f == 'hidden':
            qs = qs.filter(is_hidden=True)
        return qs


class PostToggleHiddenView(AdminRequiredMixin, View):
    def post(self, request, pk):
        p = Post.objects.get(pk=pk)
        p.is_hidden = not p.is_hidden
        p.save(update_fields=['is_hidden'])
        return JsonResponse({'is_hidden': p.is_hidden})


class PostDeleteView(AdminRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('dashboard:posts')
    template_name = 'dashboard/confirm_delete.html'


class CommentManageListView(AdminRequiredMixin, ListView):
    template_name = 'dashboard/comments.html'
    paginate_by = 30
    context_object_name = 'comments'
    queryset = Comment.objects.select_related('author', 'post').order_by('-created_at')


class CommentDeleteView(AdminRequiredMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('dashboard:comments')
    template_name = 'dashboard/confirm_delete.html'


class BroadcastView(AdminRequiredMixin, View):
    def post(self, request):
        text = request.POST.get('text', '').strip()
        if text:
            for u in User.objects.filter(is_active=True):
                Notification.objects.create(recipient=u, actor=request.user,
                                            kind='system', text=text)
        return JsonResponse({'ok': True})
