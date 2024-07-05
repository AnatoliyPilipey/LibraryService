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
    borrow_date = models.DateField()
    expected_return = models.DateField()
    actual_return = models.DateField(null=True)
    book_id = models.IntegerField()
    user_id = models.IntegerField(
    )

    def __str__(self):
        return self.expected_return
