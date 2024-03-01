# ВАРИАНТ 2
#
# from calendar import calendar
# from datetime import datetime, timedelta
# from celery import shared_task
# from smtplib import SMTPException
# from django.core.mail import send_mail
# from config import settings
# from client_service.models import Logs, SettingMailing
# from django.utils import timezone
# from django.db.models import QuerySet
#
# def mail_log(mailing, last_success_time):
#     status = True
#     error_message = ''
#     try:
#         send_mail(
#             subject=mailing.message.title,
#             message=mailing.message.text,
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[client.email for client in mailing.recipients.all()],
#             fail_silently=False
#         )
#         status = True
#         error_message = 'OK'
#
#     except SMTPException as error:
#         status = False
#         error_message = error
#     finally:
#         Logs.objects.create(
#             time=last_success_time,
#             status_try=status,
#             server_response=error_message,
#             mailing=mailing,
#             owner=mailing.owner
#         )
#
# @shared_task()
# def sort_mailing():
#
#     # Получаем все активные настройки рассылки
#     active_mailings: QuerySet = SettingMailing.objects.filter(is_active=True).exclude(status='Завершена')
#     current_time = timezone.localtime(timezone.now())
#     now: str = current_time.strftime('%Y-%m-%d %H:%M')
#     for mailing in active_mailings:
#         if mailing.end_time.strftime('%Y-%m-%d %H:%M') < now:
#             mailing.status = 'Завершена'
#             mailing.save()
#             continue
#         if mailing.start_time.strftime('%Y-%m-%d %H:%M') <= now <= mailing.end_time.strftime('%Y-%m-%d %H:%M'):
#             mailing.status = "Запущена"
#             mailing.save()
#
#         last_success_time = None
#         last_success = Logs.objects.filter(mailing=mailing, status_try=True).order_by('time')
#         if last_success:
#             last_success_time = last_success.first().time
#             last_success_time: str = last_success_time.strftime('%Y-%m-%d %H:%M')
#             print(f"DEBAG, {last_success_time}")
#             if last_success_time < now:
#                 if mailing.periodicity == "Раз в день":
#                     last_success_time = current_time + timedelta(days=1)
#                     mailing.save()
#                 elif mailing.periodicity == "Раз в неделю":
#                     last_success_time = current_time + timedelta(days=7)
#                     mailing.save()
#                 elif mailing.periodicity == "Раз в месяц":
#                     today = datetime.today()
#                     days = calendar.monthrange(today.year, today.month)[1]
#                     last_success_time = current_time + timedelta(days=days)
#                     mailing.save()
#                 if last_success_time == now:
#                     mail_log(mailing, last_success_time)
#
#         else:
#             last_success_time == current_time
#             print(f'DEBAG_DEBAG{last_success_time}')
#             mail_log(mailing, last_success_time)


#ВАРИАНТ 1

from calendar import calendar
from datetime import datetime, timedelta
from celery import shared_task
from smtplib import SMTPException
from django.core.mail import send_mail
from config import settings
from client_service.models import Logs, SettingMailing
from django.utils import timezone
from django.db.models import QuerySet


@shared_task()
def sort_mailing():
    # Получаем все активные настройки рассылки
    active_mailings: QuerySet = SettingMailing.objects.filter(is_active=True)
    current_time = timezone.localtime(timezone.now())
    now: str = current_time.strftime('%Y-%m-%d %H:%M')
    for mailing in active_mailings:
        # Проверяем, находится ли время рассылки в заданном интервале
        if mailing.start_time >= current_time:
            mailing.status = "Создана"
            mailing.save()
        elif mailing.end_time <= current_time:
            mailing.status = "Завершена"
            mailing.save()
        elif mailing.start_time.strftime('%Y-%m-%d %H:%M') <= now <= mailing.end_time.strftime('%Y-%m-%d %H:%M'):
            mailing.status = "Запущена"
            mailing.save()
            # Определяем периодичность рассылки
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
                    log = Logs.objects.create(
                        status_try=status,
                        server_response=error_message,
                        mailing=mailing,
                        owner=mailing.owner
                    )
                    log.save()
            elif mailing.next_send >= mailing.end_time:
                mailing.status = "Завершена"
                mailing.save()
