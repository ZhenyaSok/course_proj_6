from django import forms

from materials.models import Material


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'





class MaterialForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Material
        fields = 'title', 'body', 'image'