from django.forms import ValidationError
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from leads.models import Electronics, Books, HomeAndKitchen, HealthAndBeauty, SoftwareAndMobileApps, ClothingAndAccessories, ToolsAndHome, SportsAndOutdoors, MoviesAndTv, ToyAndGames, GroceryAndGourMetFood, OfficeProducts, PetSupplies, AutoMotiveAndIndustrial

from leads.serializers import ElectronicsLeadsDataSerializer, BooksLeadsDataSerializer, HomeAndKitchenLeadsDataSerializer, HealthAndBeautyLeadsDataSerializer, SoftwareAndMobileAppsLeadsDataSerializer, ClothingAndAccessoriesLeadsDataSerializer, ToolsAndHomeLeadsDataSerializer, SportsAndOutdoorsLeadsDataSerializer, MoviesAndTvLeadsDataSerializer, ToyAndGamesLeadsDataSerializer, GroceryAndGourMetFoodLeadsDataSerializer, OfficeProductsLeadsDataSerializer, PetSuppliesLeadsDataSerializer, AutoMotiveAndIndustrialLeadsDataSerializer

# Create your views here.


class helperGlobalFunction:
    category_mapping = {
        "1": [Electronics, ElectronicsLeadsDataSerializer],
        "2": [Books, BooksLeadsDataSerializer],
        "3": [HomeAndKitchen, HomeAndKitchenLeadsDataSerializer],
        "4": [HealthAndBeauty, HomeAndKitchenLeadsDataSerializer],
        "5": [SoftwareAndMobileApps, SoftwareAndMobileAppsLeadsDataSerializer],
        "6": [ClothingAndAccessories, ClothingAndAccessoriesLeadsDataSerializer],
        "7": [ToolsAndHome, ToolsAndHomeLeadsDataSerializer],
        "8": [SportsAndOutdoors, SportsAndOutdoorsLeadsDataSerializer],
        "9": [MoviesAndTv, MoviesAndTvLeadsDataSerializer],
        "10": [ToyAndGames, ToyAndGamesLeadsDataSerializer],
        "11": [GroceryAndGourMetFood, GroceryAndGourMetFoodLeadsDataSerializer],
        "12": [OfficeProducts, OfficeProductsLeadsDataSerializer],
        "13": [PetSupplies, PetSuppliesLeadsDataSerializer],
        "14": [AutoMotiveAndIndustrial, AutoMotiveAndIndustrialLeadsDataSerializer],
    }

    def getCategoryWiseTable(self, category_id):
        if (category_id in self.category_mapping):
            return self.category_mapping[category_id]