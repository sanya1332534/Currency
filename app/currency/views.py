from django.http.response import HttpResponse
from django.shortcuts import render

from currency.models import Rate, ContactUs


def rate_list(request):
    rates = Rate.objects.all()
    context = {
        'rates': rates
    }
    return render(request, 'rate_list.html', context)


def contact_us_list(request):
    feedbacks = ContactUs.objects.all()
    context = {
        'feedbacks': feedbacks
    }

    return render(request, 'contactus_list.html', context)
