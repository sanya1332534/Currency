from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_yaml.renderers import YAMLRenderer
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from currency.api.paginators import RatePagination, ContactUsPagination, SourcePagination
from currency.api.serializers import RateSerializer, SourceSerializer, ContactUsSerializer
from currency.api.throtling import RateThrottle
from currency.choices import CurrencyTypeChoices
from currency.constants import LATEST_RATES_CACHE_KEY
from currency.filters import RateFilter, SourceFilter, ContactUsFilter
from currency.models import Rate, Source, ContactUs


class RateViewSet(ModelViewSet):
    queryset = Rate.objects.all().order_by('-created')
    serializer_class = RateSerializer
    # renderer_classes = (JSONRenderer, XMLRenderer, YAMLRenderer)
    pagination_class = RatePagination
    filterset_class = RateFilter
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    ordering_fields = ('buy', 'sell', 'created')
    throttle_classes = (RateThrottle,)
    permission_classes = (AllowAny,)  # delete

    @action(methods=('GET',), detail=False, serializer_class=RateSerializer)
    def latest(self, request, *args, **kwargs):
        cached_data = cache.get(LATEST_RATES_CACHE_KEY)
        if cached_data is not None:
            return Response(cached_data)

        sources = Source.objects.all()

        latest_rates = []
        for source in sources:
            for currency in CurrencyTypeChoices:
                rate = Rate.objects.filter(source=source, currency_type=currency).order_by('-created').first()

                if rate is not None:
                    latest_rates.append(RateSerializer(instance=rate).data)

        cache.set(LATEST_RATES_CACHE_KEY, latest_rates, 60 * 60 * 24 * 7)  # 1 week

        return Response(latest_rates)


class SourceViewSet(ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    renderer_classes = (JSONRenderer, XMLRenderer, YAMLRenderer)
    pagination_class = SourcePagination
    filterset_class = SourceFilter
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        filters.SearchFilter,
    )
    ordering_fields = ('code_name', 'name')
    search_fields = ['name', 'code_name']


class ContactUsViewSet(ModelViewSet):
    queryset = ContactUs.objects.all().order_by('-created')
    serializer_class = ContactUsSerializer
    renderer_classes = (JSONRenderer, XMLRenderer, YAMLRenderer)
    pagination_class = ContactUsPagination
    filterset_class = ContactUsFilter
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        filters.SearchFilter,
    )
    search_fields = ['name', 'subject', 'body', 'email']
    ordering_fields = ('name', 'created', 'subject')
