from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import requests


class SpApiDataFetchSchedule:
    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def job_function(self):
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
        self.scheduler.add_job(self.job_function, 'interval', seconds=10)
        self.scheduler.start()
