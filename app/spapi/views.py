# from apscheduler.schedulers.background import BackgroundScheduler
# from datetime import datetime
from typing import Any
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LeadsData
from .serializers import LeadsSerializer
from django.conf import settings
from django.http import JsonResponse
from requests_aws4auth import AWS4Auth
import boto3
import requests
import json


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
            return JsonResponse(credentials, status=status.HTTP_200_OK)
        else:
            error_message = f'Error: {response.get("Error", "Unknown error")}'
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LwaTokens(APIView):
    def post(self, request, *args, **kwargs):
        url = "https://api.amazon.com/auth/o2/token"

        data = {
            "grant_type": "refresh_token",
            "client_id": settings.LWA_AUTHENTICATION['LWA_APP_ID'],
            "refresh_token": settings.LWA_AUTHENTICATION['REFRESH_TOKEN'],
            "client_secret": settings.LWA_AUTHENTICATION['LWA_CLIENT_SECRET'],
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
        }

        response = requests.post(url, data=data, headers=headers)

        if response.ok:
            json_data = response.json()
            return JsonResponse(json_data, status=status.HTTP_200_OK, safe=False)
        else:
            return Response({'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TokenManager:
    def __init__(self):
        self.access_token = None
        self.access_key_id = None
        self.secret_access_key = None
        self.session_token = None

    def generateNewLwaToken(self):
        url = "https://api.amazon.com/auth/o2/token"

        data = {
            "grant_type": "refresh_token",
            "client_id": settings.LWA_AUTHENTICATION['LWA_APP_ID'],
            "refresh_token": settings.LWA_AUTHENTICATION['REFRESH_TOKEN'],
            "client_secret": settings.LWA_AUTHENTICATION['LWA_CLIENT_SECRET'],
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
        }

        response = requests.post(url, data=data, headers=headers)

        if response.ok:
            json_data = response.json()
            self.access_token = json_data.get('access_token')
            return True
        else:
            return False

    def generateNewStsKeysAndToken(self):
        sts_client = boto3.client("sts")
        role_arn = settings.LWA_AUTHENTICATION['ROLE_ARN']
        role_session_name = "sp-api"

        response = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=role_session_name
        )
        if response.get('Credentials'):
            credentials = response['Credentials']
            self.access_key_id = credentials['AccessKeyId']
            self.secret_access_key = credentials['SecretAccessKey']
            self.session_token = credentials['SessionToken']
            return True
        else:
            return False


class GetDataFromSpApi(APIView):
    def __init__(self):
        self.tokens_manager = TokenManager()
        self.tokens_manager.generateNewLwaToken()
        self.tokens_manager.generateNewStsKeysAndToken()
        self.LISTPRICENOTFOUND = -1

    def fetchCatalogItemApiData(self, asin, marketplace_id):
        path = f"/catalog/2022-04-01/items/{asin}?marketplaceIds={marketplace_id}&includedData=attributes,identifiers,images,productTypes,salesRanks,summaries"
        method = 'GET'
        host = 'sellingpartnerapi-na.amazon.com'
        region = 'us-east-1'

        auth = AWS4Auth(
            self.tokens_manager.access_key_id,
            self.tokens_manager.secret_access_key,
            region,
            method,
            'execute-api',
            session_token=self.tokens_manager.session_token
        )

        url = f"https://{host}{path}"

        response = requests.get(url, auth=auth, headers={
                                'x-amz-access-token': self.tokens_manager.access_token})
        if (response.ok):
            return response.json()
        return False

    def fetchAmazonFbaFees(self, asin, list_price, marketplace_id):
        payload = {
            "FeesEstimateRequest": {
                "MarketplaceId": marketplace_id,
                "PriceToEstimateFees": {
                    "ListingPrice": {
                        "CurrencyCode": "CAD",
                        "Amount": list_price
                    },
                    "Shipping": {
                        "CurrencyCode": "CAD",
                        "Amount": 0
                    },
                    "Points": {
                        "PointsNumber": 0,
                        "PointsMonetaryValue": {
                            "CurrencyCode": "CAD",
                            "Amount": 0
                        }
                    }
                },
                "Identifier": "sh224",
                "IsAmazonFulfilled": "true"
            }
        }
        body = json.dumps(payload)

        headers = {
            'User-Agent': 'MyAmazonApp/1.0 (Language=JavaScript;)',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-amz-access-token': self.tokens_manager.access_token,
        }

        path = f"/products/fees/v0/items/{asin}/feesEstimate"
        method = 'POST'
        host = 'sellingpartnerapi-na.amazon.com'
        region = 'us-east-1'

        auth = AWS4Auth(
            self.tokens_manager.access_key_id,
            self.tokens_manager.secret_access_key,
            region,
            method,
            'execute-api',
            session_token=self.tokens_manager.session_token
        )
        url = f"https://{host}{path}"

        response = requests.post(url, auth=auth, headers=headers, data=body)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Request failed with status code {response.status_code}")

    def fetchProductPriceData(self, asin, marketplace_id):

        path = f"/products/pricing/v0/items/{asin}/offers?MarketplaceId={marketplace_id}&ItemCondition=New&CustomerType=Consumer"
        method = 'GET'
        host = 'sellingpartnerapi-na.amazon.com'
        region = 'us-east-1'

        auth = AWS4Auth(
            self.tokens_manager.access_key_id,
            self.tokens_manager.secret_access_key,
            region,
            method,
            'execute-api',
            session_token=self.tokens_manager.session_token
        )

        url = f"https://{host}{path}"

        response = requests.get(url, auth=auth, headers={
                                'x-amz-access-token': self.tokens_manager.access_token})

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Request failed with status code {response.status_code}")

    def get(self, request, *args, **kwargs):
        leads_data = {
            "asin": "",
            "product_image_url": "",
            "product_name": "",
            "amazon_fba_estimated_fees": "",
            "estimated_sales_rank": "",
            "amazon_price": "",
            "number_of_sellers_on_listing": "",
        }

        asin = request.query_params.get('asin')
        marketplace_id = request.query_params.get('marketplaceId')
        list_price = self.LISTPRICENOTFOUND

        if not asin or not marketplace_id:
            return Response({'error': 'Both "asin" and "marketplaceId" are required in the query parameters'},
                            status=status.HTTP_400_BAD_REQUEST)

        catalog_json_data = self.fetchCatalogItemApiData(asin, marketplace_id)

        if "asin" in catalog_json_data:
            leads_data["asin"] = catalog_json_data["asin"]
        if "attributes" in catalog_json_data \
                and catalog_json_data["attributes"] \
                and "item_name" in catalog_json_data["attributes"] \
                and catalog_json_data["attributes"]["item_name"] \
                and len(catalog_json_data["attributes"]["item_name"]) > 0 \
                and "values" in catalog_json_data["attributes"]["item_name"][0]:
            leads_data["product_name"] = catalog_json_data["attributes"]["item_name"][0]["value"]
        if "images" in catalog_json_data \
                and catalog_json_data["images"] \
                and len(catalog_json_data["images"]) > 0 \
                and "images" in catalog_json_data["images"][0] \
                and catalog_json_data["images"][0]["images"] \
                and len(catalog_json_data["images"][0]["images"]) > 0 \
                and "link" in catalog_json_data["images"][0]["images"][0]:
            leads_data["product_image_url"] = catalog_json_data["images"][0]["images"][0]["link"]

        if "salesRanks" in catalog_json_data \
                and catalog_json_data["salesRanks"] \
                and "displayGroupRanks" in catalog_json_data["salesRanks"][0] \
                and catalog_json_data["salesRanks"][0]["displayGroupRanks"] \
                and catalog_json_data["salesRanks"][0]["displayGroupRanks"][0] \
                and "rank" in catalog_json_data["salesRanks"][0]["displayGroupRanks"][0]:
            leads_data["estimated_sales_rank"] = catalog_json_data["salesRanks"][0]["displayGroupRanks"][0]["rank"]

        if "attributes" in catalog_json_data and catalog_json_data["attributes"]:
            list_price_data = catalog_json_data["attributes"].get("list_price")
            if list_price_data is not None and list_price_data:
                list_price_value = list_price_data[0]["value"]
                leads_data["amazon_price"] = list_price_value

        if list_price != self.LISTPRICENOTFOUND:
            amazon_fba_json_data = self.fetchAmazonFbaFees(
                asin, list_price, marketplace_id)
            if "payload" in amazon_fba_json_data \
                    and "FeesEstimateResult" in amazon_fba_json_data["payload"] \
                    and "FeesEstimate" in amazon_fba_json_data["payload"]["FeesEstimateResult"] \
                    and "TotalFeesEstimate" in amazon_fba_json_data["payload"]["FeesEstimateResult"]["FeesEstimate"] \
                    and "Amount" in amazon_fba_json_data["payload"]["FeesEstimateResult"]["FeesEstimate"]["TotalFeesEstimate"]:
                leads_data["amazon_fba_estimated_fees"] = amazon_fba_json_data["payload"][
                    "FeesEstimateResult"]["FeesEstimate"]["TotalFeesEstimate"]["Amount"]
        product_price_json_data = self.fetchProductPriceData(
            asin, marketplace_id)
        if "payload" in product_price_json_data\
                and product_price_json_data["payload"] \
                and "Offers" in product_price_json_data["payload"] \
                and product_price_json_data["payload"]:
            leads_data["number_of_sellers_on_listing"] = len(
                product_price_json_data["payload"]["Offers"])

        return JsonResponse(leads_data, status=status.HTTP_200_OK, safe=False)

        # if response.ok:
        #     json_data = response.json()
        #     return JsonResponse(leads_data, status=status.HTTP_200_OK, safe=False)
        # else:
        #     return Response({'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
