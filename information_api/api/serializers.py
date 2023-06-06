from core.models import Menu, Button, TelegramUser
from rest_framework import serializers

class ButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Button
        fields = "__all__"

class MenuSerializer(serializers.ModelSerializer):
    Menu = ButtonSerializer(many=True, read_only=True)
    class Meta:
        model = Menu
        fields = ['name', 'image', 'Menu']

class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = '__all__'