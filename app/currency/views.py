import re

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import (
    CreateView, UpdateView,
    DeleteView, DetailView, TemplateView
)
from django_filters.views import FilterView
from django.urls import reverse_lazy

from currency.filters import RateFilter, ContactUsFilter, SourceFilter
from currency.forms import SourceForm, RateForm, ContactUsForm
from currency.models import Rate, ContactUs, Source
from currency.tasks import send_email_in_background


class RateListView(FilterView):
    queryset = Rate.objects.all().select_related('source').order_by('-created')
    template_name = 'rate_list.html'
    paginate_by = 30
    filterset_class = RateFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        query_parameters = self.request.GET.urlencode()

        context['filter_params'] = re.sub(r'page=\d+', '', query_parameters).lstrip('&')

        return context


class RateCreateView(CreateView):
    form_class = RateForm
    success_url = reverse_lazy('currency:rate-list')
    template_name = 'rate_create.html'


class RateAccessMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class RateUpdateView(RateAccessMixin, UpdateView):
    model = Rate
    form_class = RateForm
    success_url = reverse_lazy('currency:rate-list')
    template_name = 'rate_update.html'


class RateDeleteView(RateAccessMixin, DeleteView):
    model = Rate
    success_url = reverse_lazy('currency:rate-list')
    template_name = 'rate_delete.html'


class RateDetailView(LoginRequiredMixin, DetailView):
    model = Rate
    template_name = 'rate_detail.html'
    login_url = 'login'


class ContactUsListView(FilterView):
    queryset = ContactUs.objects.all().order_by('-created')
    template_name = 'contactus_list.html'
    paginate_by = 30
    filterset_class = ContactUsFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        query_parameters = self.request.GET.urlencode()

        context['filter_params'] = re.sub(r'page=\d+', '', query_parameters).lstrip('&')

        return context


class ContactUsCreateView(CreateView):
    model = ContactUs
    template_name = 'contactus_create.html'
    success_url = reverse_lazy('currency:index')
    fields = (
        'name',
        'email',
        'subject',
        'body',
    )

    def form_valid(self, form):
        redirect = super().form_valid(form)
        send_email(self.object)

        return redirect


def send_email(contact_us):
    subject = 'User contact us'
    body = f'''
            Name: {contact_us.name}
            Email: {contact_us.email}
            Subject: {contact_us.subject}
            Body: {contact_us.body}
            '''
    send_email_in_background.apply_async(
        kwargs={
            'subject': subject,
            'body': body
        }
    )


class ContactUsUpdateView(UpdateView):
    model = ContactUs
    form_class = ContactUsForm
    success_url = reverse_lazy('currency:contactus-list')
    template_name = 'contactus_update.html'


class ContactUsDeleteView(DeleteView):
    model = ContactUs
    success_url = reverse_lazy('currency:contactus-list')
    template_name = 'contactus_delete.html'


class ContactUsDetailView(DetailView):
    model = ContactUs
    template_name = 'contactus_detail.html'


class SourceListView(FilterView):
    queryset = Source.objects.all()
    template_name = 'source_list.html'
    paginate_by = 30
    filterset_class = SourceFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        query_parameters = self.request.GET.urlencode()

        context['filter_params'] = re.sub(r'page=\d+', '', query_parameters).lstrip('&')

        return context


class SourceCreateView(CreateView):
    form_class = SourceForm
    success_url = reverse_lazy('currency:source-list')
    template_name = 'source_create.html'


class SourceUpdateView(UpdateView):
    model = Source
    form_class = SourceForm
    success_url = reverse_lazy('currency:source-list')
    template_name = 'source_update.html'


class SourceDeleteView(DeleteView):
    model = Source
    success_url = reverse_lazy('currency:source-list')
    template_name = 'source_delete.html'


class SourceDetailView(DetailView):
    model = Source
    template_name = 'source_details.html'


class IndexView(TemplateView):
    template_name = 'index.html'
