from django.forms import ModelForm

from client.models import Client
from client_service.models import MessageMailing, SettingMailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class SettingMailingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = SettingMailing
        fields = ('start_time', 'end_time', 'periodicity', 'recipients', 'owner', 'message', 'status',)


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = MessageMailing
        fields = ('title', 'text',)
