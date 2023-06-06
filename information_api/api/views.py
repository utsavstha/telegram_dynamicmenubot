from django.shortcuts import render

# Create your views here.
from api.serializers import MenuSerializer, TelegramUserSerializer
from core.models import Menu, TelegramUser
from rest_framework import viewsets, generics, permissions, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse

class MenuViewSet(viewsets.ViewSet):
    queryset = Menu.objects.all()
    permission_classes = (permissions.AllowAny,)

    def list(self, request):
        # item = Menu.objects.filter(menu_type="main").first()
        item = get_object_or_404(self.queryset, menu_type="main")
        serializer = MenuSerializer(item)
        # serializer = get_object_or_404(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        print(pk)
        item = get_object_or_404(self.queryset, id=pk)
        serializer = MenuSerializer(item)
        return Response(serializer.data)
    
class TelegramuserViewSet(viewsets.ViewSet):
    queryset = TelegramUser.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        print(request)
        try:
            data = JSONParser().parse(request)
            print(data)
            telegram_id = data["telegram_id"]
            telegram_user = TelegramUser.objects.filter(telegram_id=telegram_id)
            if len(telegram_user) < 1:
                telegramUserSerializer = TelegramUserSerializer(data=data)
                if telegramUserSerializer.is_valid():
                    telegramUserSerializer.save()
                return JsonResponse(telegramUserSerializer.data, status=201)
            else:
                return Response({"error": "user already registred"})
        except Exception as e:
            print(e)
            return Response({"error": "user already registred"})
            