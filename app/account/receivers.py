import re

from django.db.models.signals import pre_save
from django.dispatch import receiver

from account.models import User


@receiver(pre_save, sender=User)
def lower_user_email(instance, **kwargs):
    # print('BEFORE SAVE IN SIGNALS')
    instance.email = instance.email.lower()


@receiver(pre_save, sender=User)
def fix_user_phone(instance, **kwargs):
    instance.phone = re.sub(r'\D', '', instance.phone)


# @receiver(post_save, sender=User)
# def lower_user_email(instance, **kwargs):
#     print('POST SAVE IN SIGNALS')
