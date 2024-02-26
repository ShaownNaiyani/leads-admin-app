from apscheduler.schedulers.background import BackgroundScheduler
from django.core.cache import cache
from datetime import datetime
import requests


class SpApiDataFetchSchedule:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.access_token = None
        self.access_key_id = None
        self.secret_access_key = None
        self.session_token = None
        self.expires_in = None

    def getAutheticationTokenForSp(self):

        # api call for sts credentials
        stsTokenEndPointUrl = 'http://localhost:8000/spapi/api/get_sts_credentials'
        getStsCredentials = requests.get(stsTokenEndPointUrl)
        if getStsCredentials.status_code == 200:
            sts_credentials_data = getStsCredentials.json()
            self.access_key_id = sts_credentials_data['AccessKeyId']
            self.secret_access_key = sts_credentials_data['SecretAccessKey']
            self.session_token = sts_credentials_data['SessionToken']
            cache.set('access_key_id', self.access_key_id)
            cache.set('secret_access_key', self.secret_access_key)
            cache.set('session_token', self.session_token)

        else:
            print('sts credentials not found!!')

        # api call for lwa tokens
        lwaTokenEndPointUrl = 'http://localhost:8000/spapi/api/get_lwa_token'
        getLwaAccessToken = requests.post(lwaTokenEndPointUrl)

        if getLwaAccessToken.status_code == 200:
            response = getLwaAccessToken.json()
            self.access_token = response.get('access_token')
            cache.set('access_token', self.access_token)
        else:
            print('lwa access token not found!!')

        print(cache.get('access_key_id'))
        print(cache.get('secret_access_key'))
        print(cache.get('session_token'))
        print(cache.get('access_token'))

    def sp_api_call(self):
        from .models import LeadsData
        all_row_of_asins = LeadsData.objects.values_list('asin', flat=True)
        i = 0

        for asin in all_row_of_asins:
            endpoint_url = 'http://localhost:8000/spapi/api/get_sp_api_data'
            params = {'asin': asin, 'marketplaceId': 'A2EUQ1WTGCTBG2'}
            response = requests.get(endpoint_url, params=params)
            print(response)
            # print(asin)

    def start_scheduler(self, request, *args, **kwargs):
        self.scheduler.add_job(
            self.getAutheticationTokenForSp, 'interval', seconds=10)
        # self.scheduler.add_job(self.sp_api_call, 'interval', seconds=10)
        # self.scheduler.start()
