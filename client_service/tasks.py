from celery import shared_task
from client_service.models import SettingMailing
from client_service.services.services import finish_task, delete_task, send_mailing


@shared_task(name='send_message')
def send_message():
    print('Hello!')
# def send_message(mailing_id):
#     mailing = SettingMailing.objects.get(pk=mailing_id)
#     if finish_task(mailing):
#         delete_task(mailing)
#         print("111222222")
#         return
#     print('11111111')
#     return send_mailing(mailing)
