import pytest
from django.urls import reverse

from todo.models import Task


@pytest.mark.django_db
class TestTaskCreateView:

    @pytest.mark.parametrize("url", [
        "/todo/",
        reverse("todo:todo"),
        "/todo/filter/all",
        reverse("todo:filter", kwargs={"filter": "all"}),
        "/todo/filter/done",
        reverse("todo:filter", kwargs={"filter": "done"}),
    ])
    def test_for_unauthenticated_user(self, client, url, user):
        """ Unauthenticated user should be redirected to login page. """
        response = client.get(url)

        assert response.status_code == 302
        assert "user/login/?next=/" in response.url
        assert "todo/todo" in response.url or "todo/filter/"

    @pytest.mark.parametrize("url", [
        "/todo/",
        reverse("todo:todo"),
        "/todo/filter/all",
        reverse("todo:filter", kwargs={"filter": "all"}),
        "/todo/filter/done",
        reverse("todo:filter", kwargs={"filter": "done"}),
    ])
    def test_response_code_for_authenticated_user(self, client, url, user):
        client.force_login(user)
        response = client.get(url)

        assert response.status_code == 200

    def test_template_for_authenticated_user(self, todo_page_auth_response):
        templates = {temp.name for temp in todo_page_auth_response.templates}

        assert "base.html" in templates
        assert "todo/todo.html" in templates


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
        selected task archive field should be unaffected.
        """
        assert len(Task.objects.filter(archive=True)) == 0
        assert len(Task.objects.filter(archive=False)) == 1

        response = client.post(url)

        assert response.status_code == 302
        assert "user/login/?next=/todo/delete/" in response.url
        assert len(Task.objects.filter(archive=False)) == 1

    @pytest.mark.parametrize("url", [
        "/todo/delete/1/all",
        reverse("todo:delete", kwargs={"pk": 1, "selection": "all"}),
    ])
    def test_for_authenticated_user(self, client, url, user, user_task):
        """
        Test if authenticated user who is owner of a task can archive it.
        User should be redirected to filter view with appropriate selection,
        selected task archived field should be set to True.
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
        selected task archived field should be set to True.
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
    def test_for_user_with_foreign_taks(self, client, url, user_2, user_task):
        """
        Tests if user can archive other user task.
        User should be redirected to filter view with appropriate selection,
        selected task archive field should be unaffected.
        """
        assert len(Task.objects.filter(archive=True)) == 0
        assert len(Task.objects.filter(archive=False)) == 1

        client.force_login(user_2)
        response = client.post(url)

        assert response.status_code == 302
        assert "/todo/filter/all" in response.url
        assert len(Task.objects.filter(archive=True)) == 0
        assert len(Task.objects.filter(archive=False)) == 1


@pytest.mark.django_db
class TestDoneTaskView:

    @pytest.mark.parametrize("url", [
        "/todo/done/1/all",
        reverse("todo:done", kwargs={"pk": 1, "selection": "all"}),
    ])
    def test_for_unauthenticated_user(self, client, url, user, user_task):
        """
        Test if unauthenticated user cannot complete any task.
        User should be redirected to login page,
        selected task is_done field should be unaffected.
        """
        assert len(Task.objects.filter(is_done=True)) == 0
        assert len(Task.objects.filter(is_done=False)) == 1

        response = client.post(url)

        assert response.status_code == 302
        assert "user/login/?next=/todo/done/" in response.url
        assert len(Task.objects.filter(is_done=False)) == 1

    @pytest.mark.parametrize("url", [
        "/todo/done/1/all",
        reverse("todo:done", kwargs={"pk": 1, "selection": "all"}),
    ])
    def test_for_authenticated_user(self, client, url, user, user_task):
        """
        Test if authenticated user who is owner of a task can complete it.
        User should be redirected to filter view with appropriate selection,
        selected task is_done field should be set to True.
        """
        assert len(Task.objects.filter(is_done=True)) == 0
        assert len(Task.objects.filter(is_done=False)) == 1

        client.force_login(user)
        response = client.post(url)

        assert response.status_code == 302
        assert "/todo/filter/all" in response.url
        assert len(Task.objects.filter(is_done=True)) == 1
        assert len(Task.objects.filter(is_done=False)) == 0

    @pytest.mark.parametrize("url", [
        "/todo/done/1/all",
        reverse("todo:done", kwargs={"pk": 1, "selection": "all"}),
    ])
    def test_for_superuser(self, client, url, superuser, user_task):
        """
        Tests if superuser can complete other user task.
        User should be redirected to filter view with appropriate selection,
        selected task is_done field should be set to True.
        """
        assert len(Task.objects.filter(is_done=True)) == 0
        assert len(Task.objects.filter(is_done=False)) == 1

        client.force_login(superuser)
        response = client.post(url)

        assert response.status_code == 302
        assert "/todo/filter/all" in response.url
        assert len(Task.objects.filter(is_done=True)) == 1
        assert len(Task.objects.filter(is_done=False)) == 0

    @pytest.mark.parametrize("url", [
        "/todo/done/1/all",
        reverse("todo:done", kwargs={"pk": 1, "selection": "all"}),
    ])
    def test_for_user_with_foreign_taks(self, client, url, user_2, user_task):
        """
        Tests if user can complete other user task.
        User should be redirected to filter view with appropriate selection,
        selected task is_done field should be unaffected.
        """
        assert len(Task.objects.filter(is_done=True)) == 0
        assert len(Task.objects.filter(is_done=False)) == 1

        client.force_login(user_2)
        response = client.post(url)

        assert response.status_code == 302
        assert "/todo/filter/all" in response.url
        assert len(Task.objects.filter(is_done=True)) == 0
        assert len(Task.objects.filter(is_done=False)) == 1


@pytest.mark.django_db
class TestUndoDoneTaskView:

    @pytest.mark.parametrize("url", [
        "/todo/undo/1/all",
        reverse("todo:undo", kwargs={"pk": 1, "selection": "all"}),
    ])
    def test_for_unauthenticated_user(self, client, url, user, user_task_done):
        """
        Test if unauthenticated user cannot undo completion of any task.
        User should be redirected to login page,
        selected task is_done field should be unaffected.
        """
        assert len(Task.objects.filter(is_done=True)) == 1
        assert len(Task.objects.filter(is_done=False)) == 0

        response = client.post(url)

        assert response.status_code == 302
        assert "user/login/?next=/todo/undo/" in response.url
        assert len(Task.objects.filter(is_done=True)) == 1
        assert len(Task.objects.filter(is_done=False)) == 0

    @pytest.mark.parametrize("url", [
        "/todo/undo/1/all",
        reverse("todo:undo", kwargs={"pk": 1, "selection": "all"}),
    ])
    def test_for_authenticated_user(self, client, url, user, user_task_done):
        """
        Test if authenticated user who is owner of a task can undo its
        completion. User should be redirected to filter view with appropriate
        selection, selected task is_done field should be set to False.
        """
        assert len(Task.objects.filter(is_done=True)) == 1
        assert len(Task.objects.filter(is_done=False)) == 0

        client.force_login(user)
        response = client.post(url)

        assert response.status_code == 302
        assert "/todo/filter/all" in response.url
        assert len(Task.objects.filter(is_done=True)) == 0
        assert len(Task.objects.filter(is_done=False)) == 1

    @pytest.mark.parametrize("url", [
        "/todo/undo/1/all",
        reverse("todo:undo", kwargs={"pk": 1, "selection": "all"}),
    ])
    def test_for_superuser(self, client, url, superuser, user_task_done):
        """
        Tests if superuser can undo completion of other user task.
        User should be redirected to filter view with appropriate selection,
        selected task is_done field should be set to False.
        """
        assert len(Task.objects.filter(is_done=True)) == 1
        assert len(Task.objects.filter(is_done=False)) == 0

        client.force_login(superuser)
        response = client.post(url)

        assert response.status_code == 302
        assert "/todo/filter/all" in response.url
        assert len(Task.objects.filter(is_done=True)) == 0
        assert len(Task.objects.filter(is_done=False)) == 1

    @pytest.mark.parametrize("url", [
        "/todo/undo/1/all",
        reverse("todo:undo", kwargs={"pk": 1, "selection": "all"}),
    ])
    def test_for_user_with_foreign_taks(
            self, client, url, user_2, user_task_done
    ):
        """
        Tests if user cannot undo completion of other user task.
        User should be redirected to filter view with appropriate selection,
        selected task is_done field should be unaffected.
        """
        assert len(Task.objects.filter(is_done=True)) == 1
        assert len(Task.objects.filter(is_done=False)) == 0

        client.force_login(user_2)
        response = client.post(url)

        assert response.status_code == 302
        assert "/todo/filter/all" in response.url
        assert len(Task.objects.filter(is_done=True)) == 1
        assert len(Task.objects.filter(is_done=False)) == 0
