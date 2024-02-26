from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from spapi.models import LeadsData
from .models import Electronics, Books, HomeAndKitchen, HealthAndBeauty, SoftwareAndMobileApps, ClothingAndAccessories, ToolsAndHome, SportsAndOutdoors, MoviesAndTv, ToyAndGames, GroceryAndGourMetFood, OfficeProducts, PetSupplies, AutoMotiveAndIndustrial

from .serializers import LeadsManualDataSerializer, ElectronicsLeadsDataSerializer, BooksLeadsDataSerializer, HomeAndKitchenLeadsDataSerializer, HealthAndBeautyLeadsDataSerializer, SoftwareAndMobileAppsLeadsDataSerializer, ClothingAndAccessoriesLeadsDataSerializer, ToolsAndHomeLeadsDataSerializer, SportsAndOutdoorsLeadsDataSerializer, MoviesAndTvLeadsDataSerializer, ToyAndGamesLeadsDataSerializer, GroceryAndGourMetFoodLeadsDataSerializer, OfficeProductsLeadsDataSerializer, PetSuppliesLeadsDataSerializer, AutoMotiveAndIndustrialLeadsDataSerializer

from rest_framework.pagination import LimitOffsetPagination
import csv
import requests


class LeadsManualDataViewSet(viewsets.ModelViewSet):
    queryset = LeadsData.objects.all()
    serializer_class = LeadsManualDataSerializer
    pagination_class = LimitOffsetPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UploadFilesOfLeadList(APIView):
    serializer_class = LeadsManualDataSerializer
    queryset = LeadsData.objects.all()

    def patch(self, request, *args, **kwargs):
        file = request.FILES.get('lead.csv')

        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        if not file.name.endswith('.csv'):
            return Response({'error': 'Please insert a CSV type file'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                currentAsin = row.get('asin')
                if currentAsin:
                    existing_lead = LeadsData.objects.filter(
                        asin=currentAsin).first()
                    if existing_lead:
                        serializer = self.serializer_class(
                            existing_lead, data=row, partial=True)
                    else:
                        serializer = self.serializer_class(data=row)
                else:
                    continue

                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Data imported successfully'}, status=status.HTTP_200_OK)
