from django.core.management import BaseCommand
from client_service.models import SettingMailing
from client_service.tasks import send_mailing

# для запуска: python manage.py messagerun pk рассылки

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('mailing_id', nargs=1, type=int)

    def handle(self, *args, **options) -> None:
        for mailing_id in options['mailing_id']:
            try:
                mailing = SettingMailing.objects.get(pk=mailing_id)
                send_mailing(mailing)
            except Exception:
                raise (f'Рассылка не существует')