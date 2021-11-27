from django.urls import path, include

from user import views


app_name = "user"
urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("register/", views.UserCreateView.as_view(), name="register"),
    path("", include("django.contrib.auth.urls"))
]
