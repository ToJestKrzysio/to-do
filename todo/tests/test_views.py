import pytest
from django.urls import reverse

from todo.models import Task


@pytest.mark.django_db
class TestArchiveTaskView:

    @pytest.mark.parametrize("url", [
        "/todo/delete/1/all",
        reverse("todo:delete", kwargs={"pk": 1, "selection": "all"}),
    ])
    def test_for_unauthenticated_user(self, client, url, user, user_task):
        """
        Test if unauthenticated user cannot archive any task.
        User should be redirected to login page,
        selected task should be unaffected.
        """
        assert len(Task.objects.filter(archive=False)) == 1

        response = client.post(url)

        assert response.status_code == 302
        assert "accounts/login/?next=/todo/delete/" in response.url
        assert len(Task.objects.filter(archive=False)) == 1

    @pytest.mark.parametrize("url", [
        "/todo/delete/1/all",
        reverse("todo:delete", kwargs={"pk": 1, "selection": "all"}),
    ])
    def test_for_authenticated_user(self, client, url, user, user_task):
        """
        Test if authenticated user who is owner of a task can archive it.
        User should be redirected to filter view with appropriate selection,
        selected task should be marked as archived.
        """
        assert len(Task.objects.filter(archive=True)) == 0
        assert len(Task.objects.filter(archive=False)) == 1

        client.force_login(user)
        response = client.post(url)

        assert response.status_code == 302
        assert "/todo/filter/all" in response.url
        assert len(Task.objects.filter(archive=True)) == 1
        assert len(Task.objects.filter(archive=False)) == 0

    @pytest.mark.parametrize("url", [
        "/todo/delete/1/all",
        reverse("todo:delete", kwargs={"pk": 1, "selection": "all"}),
    ])
    def test_for_superuser(self, client, url, superuser, user_task):
        """
        Tests if superuser can archive other user task.
        User should be redirected to filter view with appropriate selection,
        selected task should be marked as archived.
        """
        assert len(Task.objects.filter(archive=True)) == 0
        assert len(Task.objects.filter(archive=False)) == 1

        client.force_login(superuser)
        response = client.post(url)

        assert response.status_code == 302
        assert "/todo/filter/all" in response.url
        assert len(Task.objects.filter(archive=True)) == 1
        assert len(Task.objects.filter(archive=False)) == 0

    @pytest.mark.parametrize("url", [
        "/todo/delete/1/all",
        reverse("todo:delete", kwargs={"pk": 1, "selection": "all"}),
    ])
    def test_for_user_with_foreign_taks(
            self, client, url, user_2, user_task
    ):
        """
        Tests if user can archive other user task.
        User should be redirected to filter view with appropriate selection,
        selected task should not be marked as archived.
        """
        assert len(Task.objects.filter(archive=True)) == 0
        assert len(Task.objects.filter(archive=False)) == 1

        client.force_login(user_2)
        response = client.post(url)

        assert response.status_code == 302
        assert "/todo/filter/all" in response.url
        assert len(Task.objects.filter(archive=True)) == 0
        assert len(Task.objects.filter(archive=False)) == 1
