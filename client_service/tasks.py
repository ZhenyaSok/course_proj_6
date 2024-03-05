from calendar import calendar
from datetime import datetime, timedelta
from celery import shared_task
from smtplib import SMTPException
from django.core.mail import send_mail
from config import settings
from client_service.models import Logs, SettingMailing
from django.utils import timezone
from django.db.models import QuerySet

def mail_log(mailing, last_success_time):
    status = True
    error_message = ''
    try:
        send_mail(
            subject=mailing.message.title,
            message=mailing.message.text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email for client in mailing.recipients.all()],
            fail_silently=False
        )
        status = True
        error_message = 'OK'

    except SMTPException as error:
        status = False
        error_message = error
    finally:
        Logs.objects.create(
            time=last_success_time,
            status_try=status,
            server_response=error_message,
            mailing=mailing,
            owner=mailing.owner
        )

@shared_task()
def sort_mailing():

    # Получаем все активные настройки рассылки
    active_mailings: QuerySet = SettingMailing.objects.filter(is_active=True).exclude(status='Завершена')
    current_time = timezone.localtime(timezone.now())
    now: str = current_time.strftime('%Y-%m-%d %H:%M')
    for mailing in active_mailings:
        if mailing.end_time.strftime('%Y-%m-%d %H:%M') < now:
            mailing.status = 'Завершена'
            mailing.save()
            continue
        if mailing.start_time.strftime('%Y-%m-%d %H:%M') <= now <= mailing.end_time.strftime('%Y-%m-%d %H:%M'):
            mailing.status = "Запущена"
            mailing.save()

        last_success = Logs.objects.filter(mailing=mailing, status_try=True).order_by('time')
        if last_success:
            last_success_time = last_success.first().time
            last_success_time: str = last_success_time.strftime('%Y-%m-%d %H:%M')
            if last_success_time < now:
                PERIODICITY = {
                    "Раз в день": 1,
                    "Раз в неделю": 7,
                    "Раз в месяц": calendar.monthrange(datetime.today().year, datetime.today().month)[1]
                               }
                if current_time + timedelta(days=PERIODICITY[mailing.periodicity]) == now:
                    mail_log(mailing, now)

        else:
            mail_log(mailing, current_time)
