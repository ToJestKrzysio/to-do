import pytest
from django.urls import reverse


class TestArchiveTaskView:

    @pytest.mark.parametrize("url", [
        "/todo/delete/1/all",
        reverse("todo:delete", kwargs={"pk": 1, "selection": "all"}),
    ])
    def test_response_code_for_unauthenticated_user(self, client, url):
        response = client.post(url)
        assert response.status_code == 302
        assert "accounts/login/?next=/todo/delete/" in response.url

    @pytest.mark.parametrize("url", [
        "/todo/delete/1/all",
        reverse("todo:delete", kwargs={"pk": 1, "selection": "all"}),
    ])
    def test_response_code_for_authenticated_user(self, client, user_with_task,
                                                  url):
        client.force_login(user_with_task)
        response = client.post(url)
        assert response.status_code == 302
        assert "/todo/filter/all" in response.url
