from django.contrib import admin
from .models import Client


@admin.register(Client)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'owner')
    list_filter = ('last_name', 'first_name',)
    search_fields = ('email', 'first_name', 'last_name',)
