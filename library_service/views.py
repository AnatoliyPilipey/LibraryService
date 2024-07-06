from rest_framework import viewsets, mixins
from django.db import transaction
from datetime import date
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from library_service.permissions import IsAdminOrIfAuthenticatedReadOnly
from library_service.models import (
    Book,
    Borrowing,
    Payment,
)
from library_service.serializers import (
    BookSerializer,
    BorrowingSerializer,
    BorrowingCreateSerializer,
    BorrowingDetailSerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    """Books used in the library"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class BorrowingViewSet(viewsets.ModelViewSet):
    """Displays the current status of borrowed books"""
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == "retrieve":
            serializer = BorrowingDetailSerializer
        if self.action == "create":
            serializer = BorrowingCreateSerializer
        return serializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    @action(detail=True, methods=["post"])
    def return_borrowing(self, request, pk=None):
        borrowing = Borrowing.objects.get(id=pk)
        if not borrowing.actual_return:
            with transaction.atomic():
                book = Book.objects.get(id=borrowing.book_id)
                book.inventory += 1
                book.save()

                borrowing.actual_return = f"{date.today().strftime("%Y-%m-%d")}"
                borrowing.save()
                response_return = Response({"message": f"You returned the book"})
        else:
            response_return = Response({"message": f"The book has already been returned"})
        return response_return
