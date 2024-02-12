from django.core.management import BaseCommand
from user.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='kidswear_kub@mail.ru',
            first_name='Admin_main',
            last_name='Custom',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        user.set_password('123456')
        user.save()