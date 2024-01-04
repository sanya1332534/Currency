from django.contrib import admin
from django.urls import path, include
from currency.views import IndexView

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('auth/', include('account.urls')),
    path('currency/', include('currency.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
