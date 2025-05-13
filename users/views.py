from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.mail import send_mail
from .forms import SignUpForm

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
