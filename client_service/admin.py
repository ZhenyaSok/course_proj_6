from django.contrib import admin

from client_service.models import SettingMailing, MessageMailing, Logs
from user.models import User


@admin.register(MessageMailing)
class MessageListSettingsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'owner',)
    list_filter = ('title',)
    search_fields = ('title', 'text',)


@admin.register(SettingMailing)
class MailingListSettingsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'start_time', 'end_time', 'next_send', 'periodicity', 'status', 'is_active', 'creator',)
    list_filter = ('next_send', 'periodicity', 'status', 'creator',)
    search_fields = ('start_time', 'periodicity', 'end_time', 'creator',)


@admin.register(Logs)
class LogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'mailing', 'time', 'status', 'server_response', 'owner',)
    list_filter = ('time', 'status', 'owner',)
    search_fields = ('mailing', 'time', 'status', 'owner',)