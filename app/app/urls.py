from django.urls import path, include
from django.contrib import admin
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('spapi/', include('spapi.urls')),
    path('leads/', include('leads.urls')),
]
