from django.forms import ModelForm

from client_service.models import MessageMailing

class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class MessageForm(StyleFormMixin, ModelForm):

    class Meta:
        model = MessageMailing
        fields = '__all__'