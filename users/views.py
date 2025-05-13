from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.core.mail import send_mail

from .forms import SignUpForm, ProfileForm
from .models import User


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        send_mail(
            subject="Добро пожаловать в наш магазин!",
            message=f"Привет, {user.email}! Спасибо за регистрацию.",
            from_email=None,
            recipient_list=[user.email],
            fail_silently=True,
        )
        return response


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user
