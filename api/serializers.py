from rest_framework import serializers

from todo.models import Task


class TaskModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["archive"]
        extra_kwargs = {
            "is_done": {"read_only": True},
            "archive": {"read_only": True},
        }
