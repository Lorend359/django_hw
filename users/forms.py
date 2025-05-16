from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "phone", "country"]
        widgets = {
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
        }