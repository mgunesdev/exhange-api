from rest_framework.serializers import *


class ExchangeConvertSerializer(Serializer):
    source_amount = IntegerField(required=True)
    source_currency = CharField(required=True)
    target_currency_list = ListField(required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ExchangeListSerializer(Serializer):
    start_date = DateField(format="%Y-%m-%d", required=False)
    end_date = DateField(format="%Y-%m-%d", required=False)
    source_currency = CharField(required=False)
    target_currency_list = ListField(required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ExchangeRatesSerializer(Serializer):
    source_currency = CharField(required=True)
    target_currency_list = ListField(required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
