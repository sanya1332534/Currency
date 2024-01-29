from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.renderers import JSONRenderer
from rest_framework.filters import OrderingFilter
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_yaml.renderers import YAMLRenderer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from currency.api.paginators import RatePagination, ContactUsPagination, SourcePagination
from currency.api.serializers import RateSerializer, SourceSerializer, ContactUsSerializer
from currency.api.throtling import RateThrottle
from currency.filters import RateFilter, SourceFilter, ContactUsFilter
from currency.models import Rate, Source, ContactUs


class RateViewSet(ModelViewSet):
    queryset = Rate.objects.all().order_by('-created')
    serializer_class = RateSerializer
    renderer_classes = (JSONRenderer, XMLRenderer, YAMLRenderer)
    pagination_class = RatePagination
    filterset_class = RateFilter
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    ordering_fields = ('buy', 'sell', 'created')
    throttle_classes = (RateThrottle,)


class SourceViewSet(ReadOnlyModelViewSet):
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

