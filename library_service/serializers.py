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
            "daily",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["daily"] = float(representation["daily"])
        return representation


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book_id",
            "user_id",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "book_id",
            "expected_return",
        )

    def validate(self, data):
        if Borrowing.objects.filter(user_id=self.context["request"].auth["user_id"]).exists():
            raise serializers.ValidationError(
                "You borrowed a book and have to return it before you can borrow the next one."
            )
        return data



class BorrowingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return",
            "actual_return",
            "book_id",
            "user_id",
        )
