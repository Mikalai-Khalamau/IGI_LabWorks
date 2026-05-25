import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_about_page(client):
    r = client.get(reverse("insurance:about"))
    assert r.status_code == 200


@pytest.mark.django_db
def test_privacy_page(client):
    r = client.get(reverse("insurance:privacy"))
    assert r.status_code == 200


@pytest.mark.django_db
def test_news_list(client):
    r = client.get(reverse("insurance:news-list"))
    assert r.status_code == 200
