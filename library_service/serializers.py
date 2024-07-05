from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from library_service.models import (
    Book,
    Borrowing,
    Payment,
)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "cover",
            "inventory",
            "daile",
        )


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return",
            "actual_return",
            "book_id",
            "user_id",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "expected_return",
            "book_id",
            "user_id",
        )
