from django.urls import path

from api import views


app_name = "api"
urlpatterns = [
    path("tasks/", views.TaskListAPIView.as_view(), name="tasks"),
    path("tasks_create/", views.TaskListAPIView.as_view(), name="tasks_create")
]
