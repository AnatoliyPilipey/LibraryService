from django.db.models.signals import post_save
from django.dispatch import receiver
from library_service.models import Borrowing, Book
from user.models import User
from library_service.telegram_bot import send_telegram_message


@receiver(post_save, sender=Borrowing)
def send_borrowing_notification(sender, instance, created, **kwargs):
    if created:
        book = Book.objects.get(id=instance.book_id)
        message = f"User with id {instance.user_id} take book {book.title}"
        send_telegram_message(message)
