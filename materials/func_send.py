from django.core.mail import send_mail as send_mail_django
from django.conf import settings

def send_mail():

    send_mail_django(from_email=settings.DEFAULT_FROM_EMAIL,
                     subject='',
                     recipient_list=['kapitan_kub@mail.ru'],
                     message='привет')

