from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response 
from rest_framework import status 

# custom models 
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
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
            return Response({
                    "data": user,
                    "message": f"Hi {user['first_name']}! Thanks for signing up! You will shortly get an email with OTP. Please check  your email account varification."
                }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEmailVerifyApiView(GenericAPIView):
    def post(self, request):
        otp = request.data.get('otp')
        
        try:
            otp_object = OneTimePassword.objects.get(code=otp)
            user = otp_object.user
            if not user.is_verified: 
                user.is_verified = True 
                user.save()
                return Response({"message": "Account verified successfully!"}, status=status.HTTP_200_OK)

            return Response({"message": "Account already verified!"}, status=status.HTTP_204_NO_CONTENT)
        
        except OneTimePassword.DoesNotExist:
            return Response({"Invalid OTP!"}, status=status.HTTP_404_NOT_FOUND)


class UserLoginApiView(GenericAPIView):
    serializer_class = UserLoginSerializer 
    
    def post(self, request):
        user_data = request.data 
        serializer = self.serializer_class(data=user_data)
        
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)