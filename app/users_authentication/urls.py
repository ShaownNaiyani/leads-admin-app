from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView
# custom modules 
from .views import (
    UserRegistrationApiView,
    UserEmailVerifyApiView,
    UserLoginApiView,
    PasswordResetRequestApiView,
    PasswordResetConfirmApiView,
    PasswordResetApiView,
    TestApiView,
)


urlpatterns = [
    path("register/", UserRegistrationApiView.as_view(), name="register"),
    path("verify-email/", UserEmailVerifyApiView.as_view(), name="verify-email"),
    path("login/", UserLoginApiView.as_view(), name="login"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path("password-reset/", PasswordResetRequestApiView.as_view(), name="password-reset"),
    path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmApiView.as_view(), name="password-reset-confirm"),
    path("set-new-password/", PasswordResetApiView.as_view(), name="reset-password"),
    path("test/", TestApiView.as_view(), name="test"),
]
