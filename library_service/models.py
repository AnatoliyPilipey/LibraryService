from django.db import models


class Book(models.Model):
    HARD = "HARD"
    SOFT = "SOFT"
    COVER_CHOICES = [
        (HARD, "Hard"),
        (SOFT, "Soft"),
    ]

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.CharField(
        max_length=4,
        choices=COVER_CHOICES,
        default=HARD,
    )
    inventory = models.PositiveIntegerField()
    daily = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return = models.DateField()
    actual_return = models.DateField(null=True)
    book_id = models.IntegerField()
    user_id = models.IntegerField(
    )

    def __str__(self):
        return self.expected_return


class Payment(models.Model):
    PENDING = "PEND"
    PAID = "PAID"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (PAID, "Paid"),
    ]

    PAYMENT = "PAYM"
    FINE = "FINE"
    TYPE_CHOICES = [
        (PAYMENT, "Payment"),
        (FINE, "Fine"),
    ]
    borrowing_id = models.IntegerField()
    session_url = models.URLField(max_length=255)
    session_id = models.CharField(max_length=255)

    @property
    def money_to_pay(self):
        pass
