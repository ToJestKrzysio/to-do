from rest_framework import generics

from api import serializers
from todo.models import Task


class TaskListAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskModelSerializer


class TaskCreateListAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskModelSerializer
