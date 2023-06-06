from django.db import models
import os
MENU_TYPE = (
    ("main", "MAIN"),
    ("children", "Children"),

)
class Menu(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=5000)
    image = models.ImageField(upload_to ="uploads/", blank=True)
    menu_type = models.CharField(
        max_length=20, choices=MENU_TYPE,
        default='MAIN', null=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Menu'

class TelegramUser(models.Model):
    telegram_id = models.CharField(max_length=50)
    
    
    def __str__(self):
        return self.telegram_id

class Broadcast(models.Model):
    message = models.TextField()
    sent_users = models.IntegerField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
    class Meta:
        verbose_name_plural = 'Broadcast'

class Button(models.Model):
    menu = models.ForeignKey(Menu,related_name="Menu", on_delete=models.CASCADE)
    button_name = models.CharField(max_length=50)
    source_id = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="source_buttons", blank=True, null=True)

    source_url = models.URLField(max_length = 500, blank=True)
    def __str__(self):
        return self.button_name