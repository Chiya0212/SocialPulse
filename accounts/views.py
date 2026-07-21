from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login
from django.http import JsonResponse
from django.db.models import Q
from .forms import SignUpForm, ProfileForm
from .models import User


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('posts:feed')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


class ProfileDetailView(DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['posts'] = self.object.posts.all().order_by('-created_at')[:30]
        if self.request.user.is_authenticated:
            ctx['is_following'] = self.request.user.following.filter(
                following=self.object).exists()
        return ctx


class ProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'accounts/edit_profile.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.request.user.username})


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        qs = User.objects.exclude(id=self.request.user.id)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))
        return qs.order_by('-created_at')


class ThemeToggleView(View):
    def post(self, request):
        theme = request.POST.get('theme', 'dark')
        if theme not in ('light', 'dark', 'dusk'):
            theme = 'dark'
        if request.user.is_authenticated:
            request.user.theme = theme
            request.user.save(update_fields=['theme'])
        request.session['theme'] = theme
        return JsonResponse({'ok': True, 'theme': theme})
