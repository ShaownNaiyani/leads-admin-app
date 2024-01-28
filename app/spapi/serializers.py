from rest_framework import serializers
from .models import LeadsData


class LeadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadsData
        fields = '__all__'
