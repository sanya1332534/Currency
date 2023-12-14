from django.db import models


class CurrencyTypeChoices(models.IntegerChoices):
    USD = 2, 'Dollar'
    EUR = 1, 'Euro'
