from django.contrib import admin
from .models import Menu, Button, TelegramUser, Broadcast


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id',)
    # fields = ('message',)

@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ('message','sent_users', 'createdAt')
    fields = ('message',)

class ButtonOptionInline(admin.TabularInline):
    model = Button
    fk_name = 'menu'

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title','content', 'image')
    inlines = [
        ButtonOptionInline,
    ]