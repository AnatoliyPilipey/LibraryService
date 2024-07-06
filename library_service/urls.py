from django.urls import path, include
from rest_framework import routers
from library_service.views import (
    BookViewSet,
    BorrowingViewSet,
)


router = routers.DefaultRouter()
router.registry("book", BookViewSet)
router.registry("borrowing", BorrowingViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "library_service"
