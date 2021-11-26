from django.urls import path
from todo import views

app_name = 'todo'

urlpatterns = [
    path('', views.TaskView.as_view(), name='todo'),
    path('delete/<int:pk>', views.ArchiveTaskView.as_view(), name="delete"),
    path('done/<int:pk>', views.DoneTaskView.as_view(), name="done"),
    path('filter/<str:filter>', views.TaskView.as_view(), name="filter"),
]