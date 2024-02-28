from calendar import calendar
from datetime import datetime, timedelta
from celery import shared_task
from smtplib import SMTPException
from django.core.mail import send_mail
from config import settings
from client_service.models import Logs, SettingMailing
from django.utils import timezone


def send_mailing(mailing):
    current_time = timezone.localtime(timezone.now())
    now: str = current_time.strftime('%Y-%m-%d %H:%M')
    if mailing.start_time <= current_time < mailing.end_time:
        mailing.status = SettingMailing.STARTED
        mailing.save()

        """Отправка рассылки и создание лога рассылки"""
        message = mailing.message
        for client in mailing.recipients.all():
            try:
                send_mail(
                    subject=message.title,
                    message=message.text,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    fail_silently=False
                )

                Logs.objects.create(
                    time=mailing.start_time,
                    status_try=True,
                    server_response='OK',
                    mailing=mailing,
                    owner=client.owner
                )
                # Определяем периодичность рассылки и переносим время отправки на новое
                next_send_str: str = mailing.next_send.strftime('%Y-%m-%d %H:%M')
                if next_send_str <= now:
                    if mailing.periodicity == "Раз в день":
                        mailing.next_send = current_time + timedelta(days=1)
                        mailing.save()
                    elif mailing.periodicity == "Раз в неделю":
                        mailing.next_send = current_time + timedelta(days=7)
                        mailing.save()
                    elif mailing.periodicity == "Раз в месяц":
                        today = datetime.today()
                        days = calendar.monthrange(today.year, today.month)[1]
                        mailing.next_send = current_time + timedelta(days=days)
                        mailing.save()
                    if mailing.next_send > mailing.end_time:
                        mailing.status = "Завершена"
                        mailing.save()


            except SMTPException as error:

                Logs.objects.create(
                    time=mailing.start_time,
                    status_try=False,
                    server_response=error,
                    mailing=mailing,
                    owner=client.owner
                )

    else:
        mailing.status = SettingMailing.COMPLETED
        mailing.save()







@shared_task()
def daily_mailings():
    mailings = SettingMailing.objects.filter(periodicity="Раз в день")
    # mailings = SettingMailing.objects.all()
    if mailings.exists():
        for mailing in mailings:
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