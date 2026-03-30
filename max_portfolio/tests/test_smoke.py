from django.urls import reverse


def test_home_page(client):
    response = client.get(reverse("portfolio:home"))
    assert response.status_code == 200
    page = response.content.decode("utf-8")
    assert "themeToggle" in page
    assert "set_language" in page


def test_contact_page(client):
    response = client.get(reverse("portfolio:contact"))
    assert response.status_code == 200