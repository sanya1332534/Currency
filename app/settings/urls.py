from django.contrib import admin
from django.urls import path, include
from currency.views import IndexView

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('auth/', include('account.urls')),
    path('currency/', include('currency.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]
