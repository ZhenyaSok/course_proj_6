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
    list_display = ('pk', 'start_time', 'end_time', 'periodicity', 'status', 'owner', 'message', 'next_send',)
    list_filter = ('periodicity', 'status', 'owner',)
    search_fields = ('start_time', 'periodicity', 'end_time', 'owner',)


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'mailing', 'time', 'status_try', 'server_response',)
    list_filter = ('time', 'status_try',)
    search_fields = ('mailing', 'time', 'status_try',)