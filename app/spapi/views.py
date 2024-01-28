from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LeadsData
from .serializers import LeadsSerializer
from django.conf import settings
import boto3
import requests

# Create your views here.


class AmazonAuthenticationCreds(APIView):
    def get(self, request, *args, **kwargs):
        sts_client = boto3.client("sts")
        role_arn = settings.LWA_AUTHENTICATION['ROLE_ARN']
        role_session_name = "sp-api"

        response = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=role_session_name
        )
        if response.get('Credentials'):
            credentials = response['Credentials']
            return Response(credentials, status=status.HTTP_200_OK)
        else:
            error_message = f'Error: {response.get("Error", "Unknown error")}'
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LwaTokens(APIView):
    def post(self, request, *args, **kwargs):
        url = "https://api.amazon.com/auth/o2/token"

        # Define the request body
        data = {
            "grant_type": "refresh_token",
            "client_id": settings.LWA_AUTHENTICATION['LWA_APP_ID'],
            "refresh_token": settings.LWA_AUTHENTICATION['REFRESH_TOKEN'],
            "client_secret": settings.LWA_AUTHENTICATION['LWA_CLIENT_SECRET'],
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
        }
        print(data)

        # Send the POST request
        response = requests.post(url, data=data, headers=headers)
        print(response)

        if response.ok:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
