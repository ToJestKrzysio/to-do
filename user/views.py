from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from user.forms import CustomUserCreationForm
from user.models import CustomUser


class UserLoginView(LoginView):
    template_name = "user/login.html"


class UserLogoutView(LogoutView):
    pass


class UserCreateView(CreateView):
    template_name = "user/register.html"
    success_url = reverse_lazy("todo:todo")
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        validated_form = super().form_valid(form)
        if validated_form:
            user = authenticate(username=form.cleaned_data["username"],
                                password=form.cleaned_data["password1"])
            login(self.request, user)
        return validated_form
