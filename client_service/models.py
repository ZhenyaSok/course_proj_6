from django.db import models

from client.models import Client
from config import settings
from user.models import User

NULLABLE = {'blank': True, 'null': True}


class MessageMailing(models.Model):
    """
    суть рассылки, тема и тело сообщения!
    """
    title = models.CharField(max_length=100, verbose_name='Тема письма')
    text = models.TextField(verbose_name='Письмо')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)

    # mailing_list = models.ForeignKey('SettingMailing', on_delete=models.CASCADE, verbose_name='рассылка',
    #                                  related_name='messages', **NULLABLE)
    def __str__(self):

        return f'message title:{self.title}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ('title',)

class SettingMailing(models.Model):
    """
    Параметры настройки по которым будет осуществляться рассылка
    время рассылки;
    периодичность: раз в день, раз в неделю, раз в месяц;
    статус рассылки: завершена, создана, запущена.
    """

    DAILY = "Раз в день"
    WEEKLY = "Раз в неделю"
    MONTHLY = "Раз в месяц"

    PERIODICITY_CHOICES = [
        (DAILY, "Раз в день"),
        (WEEKLY, "Раз в неделю"),
        (MONTHLY, "Раз в месяц"),
    ]

    CREATED = 'Создана'
    STARTED = 'Запущена'
    COMPLETED = 'Завершена'

    STATUS_CHOICES = [
        (COMPLETED, "Завершена"),
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
    ]

    ACTIVE_CHOICES = ((True, 'Активна'), (False, 'На модерации'))


    recipients = models.ManyToManyField(Client, verbose_name='получатели', related_name='recipients')
    start_time = models.DateTimeField(verbose_name='Дата начала рассылки')
    end_time = models.DateTimeField(verbose_name='Дата окончания рассылки')
    periodicity = models.CharField(choices=PERIODICITY_CHOICES, max_length=50, verbose_name='Периодичность')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=CREATED, verbose_name='Статус рассылки')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)
    is_active = models.BooleanField(default=True, choices=ACTIVE_CHOICES, verbose_name='Активна')
    message = models.ForeignKey(MessageMailing, on_delete=models.SET_NULL, verbose_name='Сообщение', **NULLABLE)

    def __str__(self):
        return f'{self.recipients}'


    class Meta:
        verbose_name = 'настройки рассылок'
        verbose_name_plural = 'настройки рассылок'


class Logs(models.Model):
    """
    # Логи рассылки:
    дата и время последней попытки;
    статус попытки;
    ответ почтового сервера, если он был.
    """

    time = models.DateTimeField(verbose_name='Дата и время создания лога', auto_now_add=True)
    status_try = models.BooleanField(verbose_name='Статус попытки', **NULLABLE)
    server_response = models.CharField(max_length=1000, verbose_name='Ответ почтового сервера', **NULLABLE)
    mailing = models.ForeignKey(SettingMailing, on_delete=models.CASCADE, verbose_name='Рассылка')


    def __str__(self):
        return f'{self.time} {self.status_try}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
        ordering = ('-time',)




