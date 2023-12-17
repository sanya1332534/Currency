from django import forms

from currency.models import Source, Rate, ContactUs


class SourceForm(forms.ModelForm):

    class Meta:
        model = Source
        fields = (
            'source_url',
            'name',
        )


class RateForm(forms.ModelForm):

    class Meta:
        model = Rate
        fields = (
            'buy',
            'sell',
            'currency_type',
            'source',
        )


class ContactUsForm(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = (
            'name',
            'email',
            'subject',
            'body'
        )
