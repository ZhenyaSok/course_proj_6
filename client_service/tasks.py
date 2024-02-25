from datetime import datetime

from celery import shared_task
from smtplib import SMTPException
from django.core.mail import send_mail
from timezone_field.backends import pytz

from config import settings
from client_service.models import Logs, SettingMailing
from django.utils import timezone



def send_mailing(mailing):
    # zone = pytz.timezone(settings.TIME_ZONE)
    # current_time = datetime.datetime.now(zone)
    # if mailing.start_time <= current_time < mailing.end_time:
    #     mailing.status = SettingMailing.STARTED
    #     mailing.save()
    #     message = mailing.message
    #     for client in mailing.recipients.all():
    #         try:
    #             result = send_mail(
    #                 subject=message.title,
    #                 message=message.text,
    #                 from_email=settings.EMAIL_HOST_USER,
    #                 recipient_list=[client.email, ],
    #                 fail_silently=False
    #             )

    current_time = timezone.localtime(timezone.now())
    if mailing.start_time <= current_time < mailing.end_time:
        mailing.status = SettingMailing.STARTED
        mailing.save()
        for message in mailing.messages.all():
            for client in mailing.recipients.all():
                try:
                    result = send_mail(
                        subject=message.title,
                        message=message.text,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email],
                        fail_silently=False
                    )

                    log = Logs.objects.create(
                        time=mailing.start_time,
                        status_try=result,
                        response_server='OK',
                        mailing=mailing,
                        owner=mailing.owner
                    )
                    log.save()
                    return log
                except SMTPException as error:
                    log = Logs.objects.create(
                        time=mailing.start_time,
                        status_try=False,
                        response_server=error,
                        mailing=mailing,
                        owner=mailing.owner
                    )
                    log.save()
                return log
    else:
        mailing.status = SettingMailing.COMPLETED
        mailing.save()

@shared_task()
def daily_mailings():
    mailings = SettingMailing.objects.filter(periodicity="Раз в день")
    print(mailings)
    if mailings.exists():
        for mailing in mailings:
            print('все ок')
            send_mailing(mailing)



@shared_task()
def weekly_mailings():
    mailings = SettingMailing.objects.filter(periodicity="Раз в неделю", status="Запущена")
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)

@shared_task()
def monthly_mailings():
    mailings = SettingMailing.objects.filter(periodicity="Раз в месяц", status="Запущена")
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)
@shared_task()
def send_message():

    print('Hello!')

