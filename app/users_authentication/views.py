from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, DjangoUnicodeDecodeError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit 
from helper.utils.commonApiResponse import CommonApiResponse

# custom models
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserLogoutSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
)
from .utils import send_email_with_otp_to_user
from .models import (
    User,
    OneTimePassword,
)


class UserRegistrationApiView(GenericAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        user_registration_data = request.data
        serializer = self.serializer_class(data=user_registration_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # new user
            user = serializer.data
            # user registered successfully.
            # Now we have to send an otp through registered
            # email for email verification
            send_email_with_otp_to_user(email=user["email"], request=request)
            return CommonApiResponse(
                    message=f"Hi {user['first_name']}! Thanks for signing up! You will shortly get an email with OTP. Please check  your email account varification.",
                    data=user,
                    status_code=status.HTTP_201_CREATED
                )

        return CommonApiResponse(
            message="Registration Failed! Please try again with valid info!", 
            errors=serializer.errors, 
            status_code=status.HTTP_400_BAD_REQUEST
        )


class UserEmailVerifyApiView(GenericAPIView):
    def post(self, request):
        otp = request.data.get('otp')

        try:
            otp_object = OneTimePassword.objects.get(code=otp)
            user = otp_object.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return CommonApiResponse(message="Account verified successfully!", status_code=status.HTTP_200_OK)

            return CommonApiResponse(message="Account already verified!", status_code=status.HTTP_204_NO_CONTENT)

        except OneTimePassword.DoesNotExist:
            return CommonApiResponse(message="Invalid OTP!", status_code=status.HTTP_404_NOT_FOUND)


class UserLoginApiView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)

        if serializer.is_valid(raise_exception=True):
            return CommonApiResponse(
                message="Login successful!", 
                data=serializer.data, 
                status_code=status.HTTP_200_OK
            )

        return CommonApiResponse(
            message="Login failed!",
            errors=serializer.errors, 
            status_code=status.HTTP_401_UNAUTHORIZED, 
        )


class UserLogoutApiView(GenericAPIView):
    # for logout user should be authenticated
    serializer_class = UserLogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CommonApiResponse(
            message="Logout successfully!", 
            status_code=status.HTTP_204_NO_CONTENT
        )


class PasswordResetRequestApiView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        return CommonApiResponse(
                message="Please check your email for password reset link!",
                status_code=status.HTTP_205_RESET_CONTENT
            )


class PasswordResetConfirmApiView(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))

            user = User.objects.get(id=user_id)

            if user and PasswordResetTokenGenerator().check_token(user, token):
                return CommonApiResponse(
                    message="Please use this uidb & token for password reset request!", 
                    data={
                        "uidb64": uidb64,
                        "token": token,
                    }, 
                    status_code=status.HTTP_205_RESET_CONTENT
                )

            return CommonApiResponse(
                    message="The link is invalid or expired!",
                    status_code=status.HTTP_401_UNAUTHORIZED
                )

        except DjangoUnicodeDecodeError:
            return CommonApiResponse(
                message="Unauthorized attempt!", 
                status_code=status.HTTP_401_UNAUTHORIZED
            )


class PasswordResetApiView(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def patch(self, request):
        user_data = request.data

        serializer = self.serializer_class(data=user_data)

        serializer.is_valid(raise_exception=True)

        return CommonApiResponse(
                message="Password reset successfully! You will receive an email with your new password!", 
                status_code=status.HTTP_200_OK
            )
        

@method_decorator(ratelimit(key='user', rate='5/m', method='GET', block=True), name='dispatch')
class TestApiView(GenericAPIView):
    """Experimenting rate limit"""
    def get(self, request):
        return CommonApiResponse(
            data={"message": "Hello World!"}, 
            status=status.HTTP_200_OK
        )