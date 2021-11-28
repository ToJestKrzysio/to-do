import pytest

from django.utils import timezone

from todo.models import Task


@pytest.fixture
def new_user(client, django_user_model):
    username = "username_1"
    password = "NotVeryStrongPassword123"
    user = django_user_model.objects.create_user(username=username,
                                                 password=password)
    return user

@pytest.fixture
def user_with_task(client, django_user_model, new_user):
    Task.objects.create(is_done=False, archive=False, details="details",
                        title="Test", deadline=timezone.now(),
                        owner_id=new_user.id, pk=1)
    return new_user
