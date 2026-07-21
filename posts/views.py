from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, View
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q, Count
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm
from notifications.utils import push_notification


class FeedView(ListView):
    model = Post
    template_name = 'posts/feed.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        qs = Post.objects.filter(is_hidden=False).select_related('author').annotate(
            n_likes=Count('likes', distinct=True), n_comments=Count('comments', distinct=True))
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(content__icontains=q) | Q(author__username__icontains=q))
        if self.request.user.is_authenticated:
            following_ids = self.request.user.following.values_list('following_id', flat=True)
            qs = qs.filter(Q(privacy='public') | Q(author=self.request.user) |
                           (Q(privacy='followers') & Q(author_id__in=following_ids)))
        else:
            qs = qs.filter(privacy='public')
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            ctx['post_form'] = PostForm()
            ctx['liked_ids'] = set(self.request.user.likes.values_list('post_id', flat=True))
        return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('posts:feed')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comments'] = self.object.comments.select_related('author')
        ctx['comment_form'] = CommentForm()
        return ctx


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse('posts:detail', args=[self.object.pk])


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts:feed')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.post = post
            c.author = request.user
            c.save()
            if post.author != request.user:
                push_notification(post.author, request.user, 'comment',
                                  f'commented on your post', url=f'/post/{post.pk}/')
        return redirect('posts:detail', pk=pk)


class LikeToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
            if post.author != request.user:
                push_notification(post.author, request.user, 'like',
                                  f'liked your post', url=f'/post/{post.pk}/')
        return JsonResponse({'liked': liked, 'count': post.likes.count()})
