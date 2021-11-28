import pytest
from django.urls import reverse


@pytest.mark.parametrize("url", ["/", reverse("home:home")])
def test_home_view_status_code(client, url):
    response = client.get(url)
    assert response.status_code == 200


def test_home_view_template(get_home_view_response):
    templates = {
        template.name for template in get_home_view_response.templates
    }
    assert "home/home.html" in templates
