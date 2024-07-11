import tempfile
import os

# from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from library_service.models import Book, Borrowing
from library_service.serializers import (
    BookSerializer,
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)

BOOK_URL = reverse("library_service:book-list")
BORROWING_URL = reverse("library_service:borrowing-list")


def sample_book(**params):
    defaults = {
        "title": "Sample title",
        "author": "Author",
        "inventory": 4,
        "daily": 0.1,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


def sample_borrowing(**params):
    defaults = {
        "expected_return": "2024-07-10",
        "book_id": 1,
        "user_id": 1,
    }
    defaults.update(params)

    return Borrowing.objects.create(**defaults)


def detail_book_url(item_id):
    return reverse("library_service:book-detail", args=[item_id])


def detail_borrowing_url(item_id):
    return reverse("library_service:borrowing-detail", args=[item_id])


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UnauthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_list_book(self):
        sample_book()

        res = self.client.get(BOOK_URL)

        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_book_detail(self):
        book = sample_book()

        url = detail_book_url(book.id)
        res = self.client.get(url)

        serializer = BookSerializer(book)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book_forbidden(self):
        payload = {
            "title": "Sample title",
            "author": "Author",
            "inventory": 4,
            "daily": 0.1,
        }
        res = self.client.post(BOOK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_list_borrowing(self):
        sample_book()
        sample_borrowing()
        sample_borrowing()

        res = self.client.get(BORROWING_URL)

        borrowing = Borrowing.objects.all()
        serializer = BorrowingSerializer(borrowing, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_borrowing_detail(self):
        sample_book()
        borrowing = sample_borrowing()
        url = detail_borrowing_url(borrowing.id)
        res = self.client.get(url)

        serializer = BorrowingDetailSerializer(borrowing)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
