from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins, status
from django.db import transaction
from datetime import date
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from user.models import User
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

    @staticmethod
    def str_to_bool(value_str: str):
        if value_str == "true":
            return True
        elif value_str == "false":
            return False

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == "retrieve":
            serializer = BorrowingDetailSerializer
        if self.action == "create":
            serializer = BorrowingCreateSerializer
        return serializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    @action(detail=True, methods=["get", "post"])
    def returnn(self, request, pk=None):
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

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE")

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            user_id = self.request.query_params.get("user_id")
            is_active = self.request.query_params.get("is_active")
            is_admin = self.request.user.is_staff

            if is_admin:
                if user_id:
                    get_object_or_404(User, id=user_id)
                    queryset = queryset.filter(user_id=user_id)
                if is_active:
                    queryset = queryset.filter(actual_return__isnull=self.str_to_bool(is_active))
            else:
                if is_active in ("true", "false"):
                    queryset = queryset.filter(user_id=self.request.user.id)
                    queryset = queryset.filter(actual_return__isnull=self.str_to_bool(is_active))
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "user_id",
                type=int,
                description="Filter by user id (ex. ?user_id=2)",
            ),
            OpenApiParameter(
                "is_active",
                type=str,
                description="Filtering by active borrowings (ex. ?is_active=true or false)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Displays the current status of borrowed books"""
        is_active = request.query_params.get("is_active")
        if is_active is not None:
            if is_active.lower() not in ["true", "false"]:
                return Response({"detail": "is_active must be 'true' or 'false'"}, status=status.HTTP_400_BAD_REQUEST)

        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Info Borrowing book with detail"""
        return super().list(request, *args, **kwargs)
