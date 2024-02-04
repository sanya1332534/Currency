from rest_framework import serializers
from currency.views import send_email

from currency.models import Rate, Source, ContactUs


class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = (
            'id',
            'buy',
            'sell',
            'created',
            'source',
            'currency_type',
        )


class SourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Source
        fields = (
            'source_url',
            'name',
            'code_name',
        )


class ContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUs
        fields = (
            'created',
            'name',
            'email',
            'subject',
            'body',
        )

    def create(self, validated_data):
        contact_us = super().create(validated_data)
        send_email(contact_us)
        return contact_us
