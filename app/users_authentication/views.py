from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, DjangoUnicodeDecodeError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from rest_framework import status 

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
    

class UserLogoutApiView(GenericAPIView):
    # for logout user should be authenticated 
    serializer_class = UserLogoutSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user_data = request.data 
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Logout successfully!"}, status=status.HTTP_204_NO_CONTENT)
    

class PasswordResetRequestApiView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    
    def post(self, request):
        user_data = request.data 
        serializer = self.serializer_class(data=user_data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        
        return Response({
                "message": "Please check your email for password reset link!" 
            }, status=status.HTTP_205_RESET_CONTENT)


class PasswordResetConfirmApiView(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64)) 
        
            user = User.objects.get(id=user_id)
            
            if user and PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                        "uidb64": uidb64,
                        "token": token,
                    }, status=status.HTTP_205_RESET_CONTENT) 
            
            return Response({
                    "message": "The link is invalid or expired!"
                }, status=status.HTTP_401_UNAUTHORIZED)
            
        except DjangoUnicodeDecodeError:
            return Response({"message": "Unauthorized attempt!"}, status=status.HTTP_401_UNAUTHORIZED) 


class PasswordResetApiView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    
    def patch(self, request):
        user_data = request.data 
        
        serializer = self.serializer_class(data=user_data) 
        
        serializer.is_valid(raise_exception=True)
        
        return Response({
                "message": "We will receive an email with your new password!"
            }, status=status.HTTP_200_OK)