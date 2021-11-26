from django.urls import path

from home import views

app_name = "home"

urlpatterns = [
    path("home", views.HomeView.as_view(), name="home"),
]