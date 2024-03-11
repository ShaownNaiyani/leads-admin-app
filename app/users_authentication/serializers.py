from django.contrib.auth import authenticate 
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str 
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import TokenError, RefreshToken
from .models import User
from .utils import send_password_reset_link_to_email, send_new_password_to_email


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=64, write_only=True)
    confirm_password = serializers.CharField(min_length=8, max_length=64, write_only=True)
    
    class Meta:
        model = User 
        fields = ["email", "first_name", "last_name", "password", "confirm_password"]
        
    def validate(self, attrs):
        password = attrs.get("password", "")
        confirm_password = attrs.get("confirm_password", "")
        
        if password != confirm_password:
            raise serializers.ValidationError("Password does not matched!")
        
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=10, max_length=255)
    password = serializers.CharField(min_length=8, max_length=64, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    
    class Meta:
        model = User 
        fields = ["email", "password", "full_name", "access_token", "refresh_token"] 
        
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        request = self.context.get("request")
        
        user = authenticate(request=request, email=email, password=password)
        
        if user is None:
            raise AuthenticationFailed("Unauthorized attempt!")

        if not user.is_verified:
            raise AuthenticationFailed("Please verify your account with OTP!")
        
        # programm reach this line means there is a verified user with this email
        user_token = user.get_token
        
        return {
            "email": email,
            "full_name": user.get_full_name,
            "access_token": user_token.get("access"),
            "refresh_token": user_token.get("refresh")
        }

class UserLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    
    default_error_messages = {
        'bad_token': ('Token is expired!')
    }
    
    def validate(self, attrs):
        self.token = attrs.get("refresh_token")
        return attrs
    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist() 
        except TokenError:
            return self.fail('bad_token') 
        

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=10, max_length=255)
    
    class Meta:
        fields = ["email"]
    
    def validate(self, attrs):
        email = attrs.get("email")
        user = User.objects.get(email=email)
        
        if user:
            # convert user_id to uidb64 id for security 
            user_id = user.id 
            # 1. convert to bytes string 
            # 2. convert to safe url
            uidb64 = urlsafe_base64_encode(force_bytes(user_id))
            token = PasswordResetTokenGenerator().make_token(user=user)
            current_site_domain = get_current_site(request=self.context.get("request")).domain
            relative_link = reverse(viewname="password-reset-confirm", kwargs={'uidb64': uidb64, 'token': token})
            reset_link = f"https://{current_site_domain}{relative_link}" 
            
            email_body = f"Hi {user.first_name}! \nHere is your password reset link: {reset_link}"
            
            email_data = {
                'to': user.email,
                'subject': f"Password reset link from {current_site_domain}!",
                'body': email_body
            }
            
            send_password_reset_link_to_email(email_data)
        
        return user


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=64)
    confirm_password = serializers.CharField(min_length=8, max_length=64)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    
    class Meta:
        fields = ["password", "confirm_password", "uidb64", "token"] 
        
    def validate(self, attrs):
        try:
            password = attrs.get("password")
            confirm_password = attrs.get("confirm_password") 
            uidb64 = attrs.get("uidb64")
            token = attrs.get("token") 
            
            if password != confirm_password:
                raise AuthenticationFailed("Password does not match!", 401)

            user_id = force_str(urlsafe_base64_decode(uidb64)) 
            
            user = User.objects.get(id=user_id)
            
            if user and PasswordResetTokenGenerator().check_token(user, token):
                data = {
                    "subject": "New password!", 
                    "body": f"Hay {user.first_name}! \n Here is your new password {password}\nplease don't shear this email!",
                    "to": user.email
                } 
                
                user.set_password(password)
                user.save()
                
                send_new_password_to_email(data)
                
                return user 
            else:
                raise AuthenticationFailed("Unauthorized attempt!", 401) 
            
        except Exception as e:
            raise AuthenticationFailed("Unauthorized attempt!", 401) 