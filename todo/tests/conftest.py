import pytest
from django.urls import reverse

from django.utils import timezone

from todo.models import Task


@pytest.fixture
def user(client, django_user_model):
    username = "username_1"
    password = "NotVeryStrongPassword123"
    user = django_user_model.objects.create_user(username=username,
                                                 password=password)
    return user


@pytest.fixture
def user_2(client, django_user_model):
    username = "username_2"
    password = "NotVeryStrongPassword456"
    user = django_user_model.objects.create_user(username=username,
                                                 password=password)
    return user


@pytest.fixture
def user_task(client, django_user_model, user):
    task = Task.objects.create(is_done=False, archive=False, details="details",
                        title="Test", deadline=timezone.now(),
                        owner_id=user.id)
    return task


@pytest.fixture
def user_task_done(client, django_user_model, user):
    task = Task.objects.create(is_done=True, archive=False, details="details",
                        title="Test", deadline=timezone.now(),
                        owner_id=user.id)
    return task


@pytest.fixture
def user_task_archived(client, django_user_model, user):
    task = Task.objects.create(is_done=True, archive=False, details="details",
                        title="Test", deadline=timezone.now(),
                        owner_id=user.id)
    return task


@pytest.fixture
def superuser(client, django_user_model):
    username = "TheSuperuser"
    password = "NotVeryStrongPassword789"
    user = django_user_model.objects.create_superuser(username=username,
                                                      password=password)
    return user


@pytest.fixture
def todo_page_auth_response(client, user):
    client.force_login(user)
    return client.get(reverse("todo:todo"))
