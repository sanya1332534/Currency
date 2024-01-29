import django_filters

from currency.models import Rate, Source, ContactUs


class RateFilter(django_filters.FilterSet):

    class Meta:
        model = Rate
        fields = {
            'buy': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'sell': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'currency_type': ['exact']
        }


class ContactUsFilter(django_filters.FilterSet):
    class Meta:
        model = ContactUs
        fields = {
            'name': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'subject': ['exact', 'icontains'],
            'body': ['exact', 'icontains'],
        }


class SourceFilter(django_filters.FilterSet):
    class Meta:
        model = Source
        fields = {
            'source_url': ['exact', 'icontains'],
            'name': ['exact', 'icontains'],
        }
