from django.core.management import BaseCommand
from mimesis import Person
from mimesis.locales import Locale
from client.models import Client


def create_client():
    quantity = 6
    num = []
    person = Person(Locale.EN)
    for _ in range(quantity):
        num.append(Client(
            first_name=person.first_name(),
            last_name=person.last_name(),
            email=(person.email(domains=['example.com'], unique=True))
        ))

    return num
class Command(BaseCommand):

    def handle(self, *args, **options):
            Client.objects.bulk_create(
               create_client()
        )

# f"{''.join(first_name.split()).lower() + ''.join(last_name.split()).lower()}@skypro.ru"

