from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
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

