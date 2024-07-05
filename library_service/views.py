from rest_framework import viewsets, mixins
from library_service.permissions import IsAdminOrIfAuthenticatedReadOnly
from library_service.models import (
    Book,
    Borrowing,
    Payment,
)
from library_service.serializers import (
    BookSerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    """Books used in the library"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
