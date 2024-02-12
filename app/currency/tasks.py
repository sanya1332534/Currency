from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
import requests

from currency.constants import PRIVATBANK_CODE_NAME, MONOBANK_CODE_NAME
from currency.models import Rate, Source
from currency.choices import CurrencyTypeChoices
from currency.utils import to_2_places_decimal


@shared_task
def parse_privatbank():
    url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5'
    response = requests.get(url)
    response.raise_for_status()

    source, _ = Source.objects.get_or_create(code_name=PRIVATBANK_CODE_NAME, defaults={'name': 'PrivatBank'})

    rates = response.json()

    available_currency_types = {
        'USD': CurrencyTypeChoices.USD,
        'EUR': CurrencyTypeChoices.EUR
    }

    for rate in rates:
        buy = to_2_places_decimal(rate['buy'])
        sell = to_2_places_decimal(rate['sale'])
        currency_type = rate['ccy']

        if currency_type not in available_currency_types:
            continue

        currency_type = available_currency_types[currency_type]

        check_or_create_rate(buy, sell, currency_type, source)


@shared_task
def parse_monobank():
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    response.raise_for_status()

    source, _ = Source.objects.get_or_create(code_name=MONOBANK_CODE_NAME, defaults={'name': 'MonoBank'})

    rates = response.json()

    available_currency_types = {
        840: CurrencyTypeChoices.USD,
        978: CurrencyTypeChoices.EUR
    }

    for rate in rates:
        currency_code_a = rate.get('currencyCodeA', '')
        currency_code_b = rate.get('currencyCodeB', '')

        if currency_code_a in available_currency_types and currency_code_b == 980:
            currency_type = available_currency_types[currency_code_a]
            buy = to_2_places_decimal(str(rate['rateBuy']))
            sell = to_2_places_decimal(str(rate['rateSell']))
        else:
            continue

        check_or_create_rate(buy, sell, currency_type, source)


def check_or_create_rate(buy, sell, currency_type, source):

    last_rate = Rate.objects.filter(source=source, currency_type=currency_type).order_by('-created').first()

    if last_rate is None or last_rate.buy != buy or last_rate.sell != sell:
        Rate.objects.create(
            buy=buy,
            sell=sell,
            currency_type=currency_type,
            source=source
        )


@shared_task(autoretry_for=(ConnectionError,), retry_kwargs={
    'max_retries': 5
})
def send_email_in_background(subject, body):
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_FROM_EMAIL],
        fail_silently=False,
    )
