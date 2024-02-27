from .models import User
from rest_framework import serializers


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
    