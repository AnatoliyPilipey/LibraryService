from celery import shared_task
from datetime import date
from library_service.telegram_bot import send_telegram_message
from library_service.models import Borrowing


@shared_task
def daily_task():
    today = date.today()
    borrowing = Borrowing.objects.filter(actual_return__isnull=True)
    borrowing = borrowing.filter(expected_return__lte=today)
    if len(borrowing) < 1:
        send_telegram_message("No borrowings overdue today!")
    for borrow in borrowing:
        send_telegram_message(
            f"Book_id:{borrow.book_id} user_id:{borrow.user_id} expected_return:{borrow.expected_return}"
        )
