from django.http.response import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404

from currency.forms import SourceForm
from currency.models import Rate, ContactUs, Source


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


def source_list(request):
    sources = Source.objects.all()
    context = {
        'sources': sources
    }
    return render(request, 'source_list.html', context)


def source_create(request):

    if request.method == 'POST':
        form = SourceForm(data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/source/list/')

    else:
        form = SourceForm()

    context = {
        'form': form
    }

    return render(request, 'source_create.html', context)


def source_update(request, pk):
    source = get_object_or_404(Source, id=pk)

    if request.method == 'POST':  # 2 validate data
        form = SourceForm(request.POST, instance=source)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/source/list/')

    elif request.method == 'GET':
        form = SourceForm(instance=source)

    context = {
        'form': form
    }

    return render(request, 'source_update.html', context)


def source_delete(request, pk):
    source = get_object_or_404(Source, id=pk)

    if request.method == 'GET':  # 1 render form
        context = {
            'source': source
        }
        return render(request, 'source_delete.html', context)

    elif request.method == 'POST':
        source.delete()
        return HttpResponseRedirect('/source/list/')


def source_details(request, pk):
    source = get_object_or_404(Source, id=pk)

    context = {
        'source': source
    }
    return render(request, 'source_details.html', context)
