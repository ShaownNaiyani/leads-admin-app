from django.apps import AppConfig
from . import jobs


class SpapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spapi'

    def ready(self):
        scheduler = jobs.SpApiDataFetchSchedule()
        scheduler.start_scheduler(self)
