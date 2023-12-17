from django.urls import path

from currency.views import (
    IndexView,
    RateListView,
    RateCreateView,
    RateUpdateView,
    RateDeleteView,
    RateDetailView,
    SourceListView,
    SourceCreateView,
    SourceUpdateView,
    SourceDeleteView,
    SourceDetailView,
    ContactUsListView,
    ContactUsCreateView,
    ContactUsUpdateView,
    ContactUsDeleteView,
    ContactUsDetailView,
)

app_name = 'currency'


urlpatterns = [
    path('rate/list/', RateListView.as_view(), name='rate-list'),
    path('rate/create/', RateCreateView.as_view(), name='rate-create'),
    path('rate/update/<int:pk>/', RateUpdateView.as_view(), name='rate-update'),
    path('rate/delete/<int:pk>/', RateDeleteView.as_view(), name='rate-delete'),
    path('rate/details/<int:pk>/', RateDetailView.as_view(), name='rate-details'),
    path('source/list/', SourceListView.as_view(), name='source-list'),
    path('source/create/', SourceCreateView.as_view(), name='source-create'),
    path('source/update/<int:pk>/', SourceUpdateView.as_view(), name='source-update'),
    path('source/delete/<int:pk>/', SourceDeleteView.as_view(), name='source-delete'),
    path('source/details/<int:pk>/', SourceDetailView.as_view(), name='source-details'),
    path('contactus/list/', ContactUsListView.as_view(), name='contactus-list'),
    path('contactus/create/', ContactUsCreateView.as_view(), name='contactus-create'),
    path('contactus/update/<int:pk>/', ContactUsUpdateView.as_view(), name='contactus-update'),
    path('contactus/delete/<int:pk>/', ContactUsDeleteView.as_view(), name='contactus-delete'),
    path('contactus/details/<int:pk>/', ContactUsDetailView.as_view(), name='contactus-details'),
    path('', IndexView.as_view(), name='index'),
]
