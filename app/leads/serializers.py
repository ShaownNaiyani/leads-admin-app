from rest_framework import serializers
from spapi.models import LeadsData


class LeadsManualDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadsData
        fields = '__all__'

    # def get_fields(self):
    #     fields = super().get_fields()

    #     # Include fields with default values
    #     default_fields = [
    #         'estimated_sales_rank',
    #         'sales_rank_30_days',
    #         'sales_rank_90_days',
    #         'estimated_monthly_sales',
    #         'number_of_sellers_on_listing',
    #         'number_of_reviews',

    #         # Add other fields with default values as needed
    #     ]

    #     for field_name in default_fields:
    #         if field_name not in fields:
    #             # Manually add fields with default values to the serializer
    #             fields[field_name] = serializers.IntegerField(
    #                 default=0, read_only=True)

    #     return fields
