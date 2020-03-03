import os
from time import sleep

from celery import shared_task
from django.core.mail import send_mail

from books.models import Book

EMAIL_HOST_USER = os.getenv('EMAIL_USER')

# @shared_task
# def sleepy(duration):
#     sleep(duration)
#     return None

# @shared_task
# def send_email_task():
#     sleep(10)
#     send_mail('Celery Task Worked!',
#             'This is proof the task worked',
#                 EMAIL_HOST_USER,
#                 [''])
#     return None

@shared_task
def book_created_task(pk):
    """
    Sends email to the user after its book is created
    """
    book_instance = Book.objects.get(pk=pk)
    subject = 'Book Created Notification'
    message = f'Dear, {book_instance.author.username}, You book {book_instance.title} has been created.Thank You'
    created_mail = send_mail(subject, message, EMAIL_HOST_USER, [book_instance.author.email])
    return created_mail

@shared_task
def book_updated_task(pk):
    """
    Sends email to the user after its book is updated
    """
    book_instance = Book.objects.get(pk=pk)
    subject = 'Book Updated Notification'
    message = f'Dear, {book_instance.author.username}, You book {book_instance.title} has been created.Thank You'
    updated_mail = send_mail(subject, message, EMAIL_HOST_USER, [book_instance.author.email])
    return updated_mail