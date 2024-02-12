from django.core.mail import send_mail
from django.conf import settings


def send_mail_password(new_password, email):

    send_mail(subject='Вы сменили пароль',
        message=f'Ваш пароль: {new_password}!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
              )

def send_mail_ready(email, current_site, activation_url):
        send_mail(subject='Почти готово!',
                message=f"Завершите регистрацию, перейдя по ссылке: http://{current_site}{activation_url}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]
            )