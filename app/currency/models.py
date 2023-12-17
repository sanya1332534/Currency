from django.db import models
from django.utils.translation import gettext_lazy as _

from currency.choices import CurrencyTypeChoices


class Rate(models.Model):
    buy = models.DecimalField(_('Buy'), max_digits=6, decimal_places=2)
    sell = models.DecimalField(_('Sell'), max_digits=6, decimal_places=2)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    currency_type = models.SmallIntegerField(
        _('Currency type'),
        choices=CurrencyTypeChoices.choices,
        default=CurrencyTypeChoices.USD
    )
    source = models.CharField(_('Source'), max_length=255)

    class Meta:
        verbose_name = _('Rate')
        verbose_name_plural = _('Rates')

    def __str__(self):
        return f'{self.buy} - {self.sell} - {self.source}'


class ContactUs(models.Model):
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    name = models.CharField(_('Name'), max_length=64)
    email = models.EmailField(_('Email'), max_length=128)
    subject = models.CharField(_('Subject'), max_length=256)
    body = models.CharField(_('Body'), max_length=2048)

    class Meta:
        verbose_name = _('Contact Us')
        verbose_name_plural = _('Contact Us')

    def __str__(self):
        return f'{self.name} - {self.subject}'


class Source(models.Model):
    source_url = models.TextField(max_length=255)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.source_url} - {self.name}'

    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')


class RequestResponseLog(models.Model):
    path = models.CharField(max_length=255)
    request_method = models.CharField(max_length=10)
    time = models.IntegerField()

    def __str__(self):
        return f"{self.request_method} {self.path} - {self.time} ms"
