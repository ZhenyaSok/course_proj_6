from rest_framework import serializers
from client_service.models import SettingMailing

class SettingMailingSerializer(serializers.ModelSerializer):

    class Meta:
        model = SettingMailing
        fields = '__all__'