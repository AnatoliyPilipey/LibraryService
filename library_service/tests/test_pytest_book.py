import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from library_service.models import Book
from django.contrib.auth import get_user_model


BOOK_URL = reverse("library_service:book-list")


@pytest.mark.django_db
class TestBookViewSet:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def create_user(self):
        return get_user_model().objects.create_user("test@test.com", "testpassword")

    @pytest.fixture
    def create_admin_user(self):
        return get_user_model().objects.create_superuser("admin@example.com", "password123")

    @pytest.fixture
    def create_books(self):
        Book.objects.create(
            title="Sample title1",
            author="Author1",
            inventory=4,
            daily=0.1,
            )
        Book.objects.create(
            title="Sample title2",
            author="Author2",
            inventory=5,
            daily=0.2,
        )

    def test_get_book_list_as_authenticated_user(self, api_client, create_user, create_books):
        api_client.force_authenticate(create_user)
        response = api_client.get(BOOK_URL)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) == 2

    def test_get_book_list_as_unauthenticated_user(self, api_client, create_books, create_user):
        api_client.force_authenticate(create_user)
        response = api_client.get(BOOK_URL)

        assert response.status_code == status.HTTP_200_OK

    def test_create_book_as_admin(self, api_client, create_admin_user):
        api_client.force_authenticate(create_admin_user)
        data = {
            "title": "Sample title3",
            "author": "Author3",
            "inventory": 4,
            "daily": 0.1,
        }
        response = api_client.post(BOOK_URL, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Book.objects.filter(title="Sample title3").exists()

    def test_create_book_as_non_admin(self, api_client, create_user):
        api_client.force_authenticate(create_user)
        data = {
            "title": "Sample title4",
            "author": "Author4",
            "inventory": 4,
            "daily": 0.1,
        }
        response = api_client.post(BOOK_URL, data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN
