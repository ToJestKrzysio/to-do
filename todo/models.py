from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db import models


def default_deadline():
    return datetime.now() + timedelta(weeks=1)


class Task(models.Model):
    is_done = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    details = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    archive = models.BooleanField(default=False)
    deadline = models.DateTimeField(default=default_deadline, blank=True)

    def __str__(self):
        return f'{self.details}'

    class Meta:
        ordering = ['deadline']
