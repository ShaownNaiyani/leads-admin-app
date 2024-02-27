from django.urls import path

# custom modules 
from .views import (
    UserRegistrationApiView,
)


urlpatterns = [
    path("register/", UserRegistrationApiView.as_view(), name="register"),
    
]
