from django.contrib.auth.models import AbstractUser
from django.db import models

from client.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')

    phone = models.CharField(max_length=35, verbose_name='номер телефона', **NULLABLE)
    telegram = models.CharField(max_length=150, verbose_name='телеграм пользователя', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)

    # email_verify = models.BooleanField(default=False, verbose_name='проверка почты')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

