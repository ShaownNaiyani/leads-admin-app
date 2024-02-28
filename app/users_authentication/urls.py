from django.urls import path

# custom modules 
from .views import (
    UserRegistrationApiView,
    UserEmailVerifyApiView,
    UserLoginApiView,
)


urlpatterns = [
    path("register/", UserRegistrationApiView.as_view(), name="register"),
    path("verify-email/", UserEmailVerifyApiView.as_view(), name="verify-email"),
    path("login/", UserLoginApiView.as_view(), name="login"),
]
