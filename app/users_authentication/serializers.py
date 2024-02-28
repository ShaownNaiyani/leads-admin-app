from django.contrib.auth import authenticate 
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import User


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
    