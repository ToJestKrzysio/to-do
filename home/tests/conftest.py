import pytest
from django.urls import reverse


@pytest.fixture
def get_home_view_response(client):
    url = reverse("home:home")
    return client.get(url)
