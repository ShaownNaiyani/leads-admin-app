from django.urls import (
    path,
    include
)
from rest_framework.routers import DefaultRouter
from .views import UploadFilesOfLeadList

from leads import views

router = DefaultRouter()
router.register('leads-data', views.LeadsManualDataViewSet)

app_name = 'leads'

urlpatterns = [
    path('', include(router.urls)),
    path('leads-file-upload', UploadFilesOfLeadList.as_view(),
         name='leads-file-upload')
]
