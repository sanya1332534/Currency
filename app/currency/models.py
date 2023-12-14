from django.db import models

from currency.choices import CurrencyTypeChoices


class Rate(models.Model):
    buy = models.DecimalField(max_digits=6, decimal_places=2)
    sell = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    currency_type = models.SmallIntegerField(
        choices=CurrencyTypeChoices.choices,
        default=CurrencyTypeChoices.USD
    )
    source = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.buy} - {self.sell} - {self.source}'


class ContactUs(models.Model):
    email_from = models.EmailField()
    subject = models.CharField(max_length=64)
    message = models.TextField(max_length=1024)

    def __str__(self):
        return f'{self.email_from} - {self.subject}'


class Source(models.Model):
    source_url = models.TextField(max_length=255)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.source_url} - {self.name}'
