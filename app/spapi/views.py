# from apscheduler.schedulers.background import BackgroundScheduler
# from datetime import datetime
from typing import Any
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import LeadsData
from .serializers import LeadsSerializer
from django.conf import settings
from django.http import JsonResponse
from requests_aws4auth import AWS4Auth
import concurrent.futures
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
        # self.tokens_manager = TokenManager()
        # self.tokens_manager.generateNewLwaToken()
        # self.tokens_manager.generateNewStsKeysAndToken()
        self.LISTPRICENOTFOUND = -1

    def fetchCatalogItemApiData(self, asin, marketplace_id):
        path = f"/catalog/2022-04-01/items/{asin}?marketplaceIds={marketplace_id}&includedData=attributes,images,salesRanks"
        method = 'GET'
        host = 'sellingpartnerapi-na.amazon.com'
        region = 'us-east-1'

        # auth = AWS4Auth(
        #     self.tokens_manager.access_key_id,
        #     self.tokens_manager.secret_access_key,
        #     region,
        #     method,
        #     'execute-api',
        #     session_token=self.tokens_manager.session_token
        # )
        auth = AWS4Auth(
            cache.get('access_key_id'),
            cache.get('secret_access_key'),
            region,
            method,
            'execute-api',
            session_token=cache.get('session_token')
        )

        url = f"https://{host}{path}"

        response = requests.get(url, auth=auth, headers={
                                'x-amz-access-token': cache.get('access_token')})
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
            'x-amz-access-token': cache.get('access_token'),
        }

        path = f"/products/fees/v0/items/{asin}/feesEstimate"
        method = 'POST'
        host = 'sellingpartnerapi-na.amazon.com'
        region = 'us-east-1'

        auth = AWS4Auth(
            cache.get('access_key_id'),
            cache.get('secret_access_key'),
            region,
            method,
            'execute-api',
            session_token=cache.get('session_token')
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
            cache.get('access_key_id'),
            cache.get('secret_access_key'),
            region,
            method,
            'execute-api',
           session_token=cache.get('session_token')
        )

        url = f"https://{host}{path}"

        response = requests.get(url, auth=auth, headers={
                                'x-amz-access-token': cache.get('access_token')})

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

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_catalog = executor.submit(
                self.fetchCatalogItemApiData, asin, marketplace_id)
            # future_fba = executor.submit(fetch_fba_data)
            # future_price = executor.submit(
            #     self.fetchProductPriceData, asin, marketplace_id)

        # print(future_catalog)
        # print(future_price)
        catalog_json_data = future_catalog.result()
        # product_price_json_data = future_price.result()

        if "asin" in catalog_json_data:
            leads_data["asin"] = catalog_json_data["asin"]
        if "attributes" in catalog_json_data \
                and catalog_json_data["attributes"] \
                and "item_name" in catalog_json_data["attributes"] \
                and catalog_json_data["attributes"]["item_name"] \
                and len(catalog_json_data["attributes"]["item_name"]) > 0 \
                and "value" in catalog_json_data["attributes"]["item_name"][0]:
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

        # if "payload" in product_price_json_data\
        #         and product_price_json_data["payload"] \
        #         and "Offers" in product_price_json_data["payload"] \
        #         and product_price_json_data["payload"]:
        #     leads_data["number_of_sellers_on_listing"] = len(
        #         product_price_json_data["payload"]["Offers"])
        # return leads_data;
        return JsonResponse(data=leads_data, status=status.HTTP_200_OK, safe=False)

        # if response.ok:
        #     json_data = response.json()
        #     return JsonResponse(leads_data, status=status.HTTP_200_OK, safe=False)
        # else:
        #     return Response({'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConcurrentAPICallView(APIView):
    def get_data(self, asin):
        url = f'http://localhost:8000/spapi/api/get_sp_api_data?asin={asin}&marketplaceId=A2EUQ1WTGCTBG2'
        response = requests.get(url)
        return response

    def get(self, request):
        asins = ['B07BF2CD75', 'B08H1LBQMZ', 'B01N0O7QKJ', 'B00006IFMO', 'B007RAQTSI', 'B07PZGSWN9', 'B07XLDRB2S', 'B0025TUZ8Q', 'B08YPCDG29', 'B004QJU51K']  # Replace with your list of ASINs
        ans = [];

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Concurrently fetch data for all ASINs
            future_to_asin = {executor.submit(self.get_data, asin): asin for asin in asins}
            asin_data = []

            for future in concurrent.futures.as_completed(future_to_asin):
                asin = future_to_asin[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print(f'Fetching data for {asin} generated an exception: {exc}')
                else:
                    asin_data.append(data.json())

        # Now you have an array of dictionaries, each containing ASIN and its associated data
        for item in asin_data:
            print(item)

        # return Response('successful')
        return JsonResponse(data=asin_data, status=status.HTTP_200_OK, safe=False)
            # Concurrently fetch data for all ASINs
            # asin1 = executor.submit(self.get_data, 'B07BF2CD75')
            # asin2 = executor.submit(self.get_data, 'B08H1LBQMZ')
            # asin3 = executor.submit(self.get_data, 'B01N0O7QKJ')
            # asin4 = executor.submit(self.get_data, 'B00006IFMO')
            # asin5 = executor.submit(self.get_data, 'B007RAQTSI')
            # asin6 = executor.submit(self.get_data, 'B07PZGSWN9')
            # asin7 = executor.submit(self.get_data, 'B07XLDRB2S')
            # asin8 = executor.submit(self.get_data, 'B0025TUZ8Q')
            # asin9 = executor.submit(self.get_data, 'B08YPCDG29')
            # asin10 = executor.submit(self.get_data, 'B004QJU51K')

            # Retrieve the responses
            # response1 = asin1.result()
            # response2 = asin2.result()
            # response3 = asin3.result()
            # response4 = asin4.result()
            # response5 = asin5.result()
            # response6 = asin6.result()
            # response7 = asin7.result()
            # response8 = asin8.result()
            # response9 = asin9.result()
            # response10 = asin10.result()

        # Now you can use response1 and response2 as needed
        # print(response1)
        # print(response2)
        # print(response3)
        # print(response4)
        # print(response5)
        # print(response6)
        # print(response7)
        # print(response8)
        # print(response9)
        # print(response10)


        # return Response('successful')
