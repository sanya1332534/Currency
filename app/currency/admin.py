from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateRangeFilterBuilder

from currency.models import Rate, ContactUs, Source


@admin.register(Rate)
class RateAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'buy',
        'sell',
        'source',
        'currency_type',
        'created'
    )
    list_filter = (
        'currency_type',
        ('created', DateRangeFilterBuilder())
    )
    search_fields = (
        'buy',
        'sell',
        'source',
    )
    readonly_fields = (
        'buy',
        'sell'
    )


@admin.register(ContactUs)
class ContactUsAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'email_from',
        'subject',
        'message',
    )
    search_fields = (
        'email_from',
        'subject',
    )
    readonly_fields = (
        'email_from',
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Source)
class SourceAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'source_url',
        'name',
    )
    search_fields = (
        'source_url',
        'name',
    )

