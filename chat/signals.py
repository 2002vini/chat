from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from . models import Profile

@receiver(post_save,sender=User)
def buildprofile(sender,instance,created,**kwargs):
    if created:
        profile=Profile.objects.create(user=instance)
        profile.save()
# @receiver(post_save, sender=ChatNotification)
# def send_notification(sender, instance, created, **kwargs):
#     print("in signal")
#     if created:
#         channel_layer = get_channel_layer()
#         notification_obj = ChatNotification.objects.filter(is_seen=False, chat_sent_to=instance.chat_sent_to).count()

#         user_id = str(instance.chat_sent_to.id)
#         print("in signals")
#         data = {
#             'count':notification_obj
#         }
#         print(notification_obj)
#         async_to_sync(channel_layer.group_send)(
#             user_id, {
#                 'type':'send_notification',
#                 'value':json.dumps(data)
#             }
#         )