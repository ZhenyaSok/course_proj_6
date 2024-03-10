from django.db import models


from config import settings
NULLABLE = {'blank': True, 'null': True}

class Client(models.Model):
    """
    Клиент - получатель рассылки, которому будут отправляться рассылки
    """
    first_name = models.CharField(max_length=150, verbose_name='имя')
    last_name = models.CharField(max_length=150, verbose_name='фамилия')
    email = models.EmailField(verbose_name='почта', unique=True)
    message = models.TextField(max_length=700, verbose_name='комментарий')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'


    class Meta:
        verbose_name = 'получатель'
        verbose_name_plural = 'получатели'
        ordering = ('last_name', 'first_name',)
