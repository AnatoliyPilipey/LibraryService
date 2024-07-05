from django.contrib import admin

from .models import (
    Payment,
    Borrowing,
    Book,
)


admin.site.register(Book)
admin.site.register(Borrowing)
admin.site.register(Payment)
