from django.http.response import HttpResponse

from currency.models import Rate, ContactUs


def rate_list(request):

    results = []
    rates = Rate.objects.all()

    for rate in rates:
        results.append(
            f'ID: {rate.id}, buy: {rate.buy}, sell: {rate.sell}, type: {rate.currency_type}, '
            f'source: {rate.source}, created: {rate.created} <br>'
        )

    return HttpResponse(str(results))


def contact_us_list(request):

    results = []
    feedback = ContactUs.objects.all()

    for contact_us in feedback:
        results.append(
            f'ID: {contact_us.id}, email: {contact_us.email_from}, subject: {contact_us.subject}, '
            f'message: {contact_us.message} <br>'
        )

    return HttpResponse(str(results))
