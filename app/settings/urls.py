from django.contrib import admin
from django.urls import path

from currency.views import rate_list, contact_us_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rate/list/', rate_list),
    path('contactus/list/', contact_us_list),
]
