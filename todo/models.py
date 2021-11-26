from django.contrib.auth import get_user_model
from django.db import models


class Task(models.Model):
    is_done = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    details = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.details}'

    class Meta:
        ordering = ['-created_at']
