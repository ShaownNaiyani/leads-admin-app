# custom_middleware.py
from users_authentication.models import User
from helper.utils.commonApiResponse import CommonApiResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .utils import checkIsNeedAutheticaitonForUrl

class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authentication = JWTAuthentication()

    def __call__(self, request):
        if checkIsNeedAutheticaitonForUrl(request.path):
            response = self.get_response(request)
            return response

        access_token = request.headers.get('Authorization')
        if(access_token is None) :
            print(access_token)
            return CommonApiResponse(message='Please Provide you authorization token!!', errors='Unauthorized!!', status_code= status.HTTP_401_UNAUTHORIZED);

        user = self.validate_access_token(access_token)
        if user:
            request.user = user
        response = self.get_response(request)
        return response

    def validate_access_token(self, access_token):
       if not access_token:
        return None
       try:
            validated_token = self.jwt_authentication.get_validated_token(access_token)
            user = self.jwt_authentication.get_user(validated_token)
            return user
       except Exception as e:
            return None
