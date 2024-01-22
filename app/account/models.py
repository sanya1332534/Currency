import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static

from account.managers import UserManager


def user_directory_path(instance, filename):
    return f'avatars/user_{instance.id}/{filename}'


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.FileField(_('Avatar'), default=None, null=True, blank=True, upload_to='user_directory_path')
    phone = models.CharField(_('Phone'), max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        app_label = 'account'

    @property
    def avatar_url(self) -> str:
        if self.avatar:
            return self.avatar.url

        return static('anonymous-user.webp')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.username = uuid.uuid4()

        # print('BEFORE SAVE IN MODEL SAVE')
        instance = super().save(*args, **kwargs)
        # print('AFTER SAVE IN MODEL SAVE')
        return instance
