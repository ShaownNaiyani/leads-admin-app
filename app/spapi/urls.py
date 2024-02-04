from django.urls import path
from .views import AmazonAuthenticationCreds, LwaTokens, GetDataFromSpApi


urlpatterns = [
    path('api/get_sts_credentials',
         AmazonAuthenticationCreds.as_view(), name='sts_credentials'),
    path('api/get_lwa_token',
         LwaTokens.as_view(), name='lwa_token'),
    path('api/get_sp_api_data',
         GetDataFromSpApi.as_view(), name='get_sp_api_data')
]
