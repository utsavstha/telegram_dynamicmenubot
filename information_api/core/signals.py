from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Broadcast, TelegramUser
from .send_message_to_users import send_message_to_users
from django.utils import timezone

@receiver(pre_save, sender=Broadcast)
def handle_broadcast_save(sender, instance, **kwargs):
    print(instance)
    if instance is not None:
        # Get the list of user IDs and message text
        user_ids = list(TelegramUser.objects.values_list('telegram_id', flat=True))  # Example user IDs
        message_text = instance.message
        # print(user_ids)
        instance.sent_users = len(user_ids)

        # Call the send_message_to_users function
        send_message_to_users(user_ids, message_text, schedule=timezone.now())
