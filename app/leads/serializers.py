from rest_framework import serializers
from spapi.models import LeadsData
from .models import Electronics, Books, HomeAndKitchen, HealthAndBeauty, SoftwareAndMobileApps, ClothingAndAccessories, ToolsAndHome, SportsAndOutdoors, MoviesAndTv, ToyAndGames, GroceryAndGourMetFood, OfficeProducts, PetSupplies, AutoMotiveAndIndustrial


class LeadsManualDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadsData
        fields = '__all__'


class ElectronicsLeadsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Electronics
        fields = '__all__'


class BooksLeadsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'


class HomeAndKitchenLeadsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeAndKitchen
        fields = '__all__'


class HealthAndBeautyLeadsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthAndBeauty
        fields = '__all__'


class SoftwareAndMobileAppsLeadsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareAndMobileApps
        fields = '__all__'


class ClothingAndAccessoriesLeadsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothingAndAccessories
        fields = '__all__'


class ToolsAndHomeLeadsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolsAndHome
        fields = '__all__'


class SportsAndOutdoorsLeadsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportsAndOutdoors
        fields = '__all__'


class MoviesAndTvLeadsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoviesAndTv
        fields = '__all__'


class ToyAndGamesLeadsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToyAndGames
        fields = '__all__'


class GroceryAndGourMetFoodLeadsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroceryAndGourMetFood
        fields = '__all__'


class OfficeProductsLeadsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeProducts
        fields = '__all__'


class PetSuppliesLeadsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetSupplies
        fields = '__all__'


class AutoMotiveAndIndustrialLeadsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoMotiveAndIndustrial
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
