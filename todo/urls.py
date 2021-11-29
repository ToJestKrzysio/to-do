from django.urls import path
from todo import views

app_name = 'todo'

urlpatterns = [
    path('', views.TaskCreateView.as_view(), name='todo'),
    path('delete/<int:pk>/<str:selection>', views.ArchiveTaskView.as_view(), name="delete"),
    path('done/<int:pk>/<str:selection>', views.DoneTaskView.as_view(), name="done"),
    path('undo/<int:pk>/<str:selection>', views.UndoDoneTaskView.as_view(), name="undo"),
    path('filter/<str:filter>', views.TaskCreateView.as_view(), name="filter"),
]
