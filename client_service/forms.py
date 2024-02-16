from django.forms import ModelForm

from client.models import Client
from client_service.models import MessageMailing, SettingMailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
#
#
# class MailingSettingsForm(StyleFormMixin, ModelForm):
#     class Meta:
#         model = SettingMailing
#         fields = ('start_time', 'end_time', 'periodicity',)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         owner = kwargs.pop('initial').get('owner')
#         # if not owner.is_superuser:
#         #     self.fields['clients'].queryset = Client.objects.all().filter(owner=owner)
#         #     self.fields['message'].queryset = MessageMailing.objects.all().filter(owner=owner)



class SettingMailingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = SettingMailing
        fields = ('start_time', 'end_time', 'periodicity', 'recipients', 'creator',)


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = MessageMailing
        fields = ('title', 'text',)


# class ClientForm(ModelForm):
#     class Meta:
#         model = Client
#         fields = ('last_name', 'email', 'comment',)