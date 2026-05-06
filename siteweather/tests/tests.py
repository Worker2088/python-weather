import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

def test_example():
    assert 1 == 1


@pytest.mark.django_db
def test_user_registration_fields(client):
    url = reverse("register")

    data = {
        "username": "alex",
        "password1": "StrongPass123!",
        "password2": "StrongPass123!",
    }

    client.post(url, data)

    user = User.objects.get(username="alex")

    assert user.username == "alex"
    assert user.check_password("StrongPass123!")