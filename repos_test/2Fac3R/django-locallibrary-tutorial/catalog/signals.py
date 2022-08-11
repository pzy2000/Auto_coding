from django.dispatch import receiver
from django.db.models.signals import post_save
from notifications.signals import notify

from django.contrib.auth.models import User
from .models import Genre

from django.utils import timezone

@receiver(post_save, sender=Genre)
def notify_admins(sender, instance, **kwargs):
    """ Signal to notify admin users about post save in Genre """
    user = User.objects.get(id=1)
    admins_group = User.objects.filter(groups__name='Admin')
    class_name = sender.__name__
    new_instance_name = instance.name
    notify.send(
        user,
        recipient=admins_group,
        verb='modified',
        level='success',
        description='{0} modified ({1}) at {2}.'.format(class_name, new_instance_name, timezone.now())
    )
