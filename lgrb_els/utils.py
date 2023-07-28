from django.core.mail import send_mail

from lgrb_els import settings


def push_email(subject, message, recipient):
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, recipient,
              auth_user=settings.EMAIL_HOST_USER,
              auth_password=settings.EMAIL_HOST_PASSWORD)
