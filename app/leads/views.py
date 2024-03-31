from asyncio import exceptions
from django.forms import ValidationError
from django.http import JsonResponse
from rest_framework.response import Response
from helper.utils.commonApiResponse import CommonApiResponse
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework import exceptions
from rest_framework.parsers import MultiPartParser, FormParser
from spapi.models import LeadsData
from .serializers import LeadsManualDataSerializer

from helper.views import helperGlobalFunction
from rest_framework.pagination import LimitOffsetPagination
import csv
import requests
import logging

logger = logging.getLogger(__name__)

class LeadsManualDataViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    queryset = LeadsData.objects.none()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helperGlobalFunctionObj = helperGlobalFunction()

    def get_serializer_class(self):
        category_id = self.request.query_params.get('category_id')
        selected_category_serializer = self.helperGlobalFunctionObj.getCategoryWiseTable(
            category_id)
        if selected_category_serializer is None:
            raise exceptions.ValidationError("category_id not found!")
        return selected_category_serializer[1]

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        selected_category = self.helperGlobalFunctionObj.getCategoryWiseTable(
            category_id)
        if selected_category is None:
            raise exceptions.ValidationError("category_id not found!")
        selected_category_model = selected_category[0]
        queryset = selected_category_model.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UploadFilesOfLeadList(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helperGlobalFunctionObj = helperGlobalFunction()

    def patch(self, request, *args, **kwargs):
        category_id = self.request.query_params.get('category_id')
        selected_category = self.helperGlobalFunctionObj.getCategoryWiseTable(
            category_id)
        if selected_category is None:
            raise exceptions.ValidationError("category_id not found!")

        serializer_class = selected_category[1];
        category_model = selected_category[0];

        file = request.FILES.get('lead.csv')
        print(file);

        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        if not file.name.endswith('.csv'):
            return Response({'error': 'Please insert a CSV type file'}, status=status.HTTP_400_BAD_REQUEST)

        content = file.read(1024).decode('utf-8')
        delimiter = '\t' if '\t' in content else ','
        file.seek(0)

        try:
            decoded_file = file.read().decode('utf-8').splitlines()
            print(delimiter)
            reader = csv.DictReader(decoded_file, delimiter=delimiter)
            # reader = csv.DictReader(decoded_file)
            for row in reader:
                print(row)
                currentAsin = row.get('asin')
                if currentAsin:
                    existing_lead = category_model.objects.filter(
                        asin=currentAsin).first()
                    if existing_lead:
                        serializer = serializer_class(
                            existing_lead, data=row, partial=True)
                    else:
                        serializer = serializer_class(data=row)

                else:
                    # logger.error(serializer.errors)
                    return CommonApiResponse(data={}, message='failed to import csv file!!', status_code=status.HTTP_400_BAD_REQUEST, errors= "Found Null object!!")

                if serializer.is_valid():
                    serializer.save()
                else:
                    logger.error(serializer.errors)
                    return CommonApiResponse(data={}, message='failed to import csv file!!', status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)


        except Exception as e:
            logger.error(str(e))
            return CommonApiResponse(message='failed to import csv file!!', errors = str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return CommonApiResponse(data=reader, message='data imported successfully!!', status_code=status.HTTP_200_OK)

