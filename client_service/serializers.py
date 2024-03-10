from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from client.models import Client


from client_service.models import SettingMailing


class SettingMailingSerializer(serializers.ModelSerializer):
    message = serializers.SlugRelatedField(slug_field='title', queryset=SettingMailing.objects.all())
    owner = serializers.SlugRelatedField(slug_field='email', queryset=SettingMailing.objects.all())
    recipients = serializers.StringRelatedField(many=True, read_only=True)


    class Meta:
        model = SettingMailing
        fields = ('id', 'periodicity', 'status', 'message', 'end_time', 'owner', 'recipients')
