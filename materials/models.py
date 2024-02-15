from django.db import models
from django.utils import timezone


NULLABLE = {'null': True}


class Material(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    body = models.TextField(max_length=1000, verbose_name='содержимое')
    image = models.ImageField(**NULLABLE, verbose_name='Изображение')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    views_count = models.IntegerField(default=0,verbose_name='просмотры')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    slug = models.CharField(max_length=100, verbose_name='slug', null=True, blank=True)


    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'

