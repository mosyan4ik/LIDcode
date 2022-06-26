import datetime
import time

from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from LIDcodeSite import settings
from .models import *
from django.core.mail import send_mail


@receiver(pre_delete, sender=Event)
def Event_delete(sender, instance, **kwargs):
    instance.image.delete(False)


@receiver(pre_delete, sender=Organizers)
def Organizers_delete(sender, instance, **kwargs):
    instance.image.delete(False)


@receiver(pre_delete, sender=Sponsors)
def Sponsors_delete(sender, instance, **kwargs):
    instance.image.delete(False)

def send(mail, event, text):
    send_mail("LIDcode event status", f"Ваша заявка регистрации на соревнование '{event}' "
                                      f"{text}",
              settings.EMAIL_HOST_USER, [mail])


@receiver(pre_save, sender=Team)
def pre_save_Team(sender, instance, **kwargs):
    if instance.approvement == 'hold':
        pass
    elif instance.approvement == 'rejected':
        send(str(instance.contactPerson.emailadress), instance.my_event, "отклонена администратором")

    elif instance.approvement == 'approved':
        eve = Event.objects.get(pk=instance.my_event.pk)
        if eve.getParticipant() < eve.numberComands:
            eve.participants.add(instance.id)
            send(str(instance.contactPerson.emailadress), instance.my_event, "принята администратором")
        else:
            instance.approvement = 'rejected'
            send(str(instance.contactPerson.emailadress), instance.my_event, "не будет рассмотрена, "
                                                                             "тк достигнуто максимальное "
                                                                             "количество команд")

