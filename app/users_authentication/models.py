from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _ 
from rest_framework_simplejwt.tokens import RefreshToken
from .managers import UserManager 


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True, editable=False) 
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email Address"))
    first_name = models.CharField(verbose_name=_("First Name"), max_length=50)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=50)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    
    # user name field for login 
    USERNAME_FIELD = "email" 
    
    # required fields for registration 
    REQUIRED_FIELDS = ["first_name", "last_name"]
    
    objects = UserManager()
    
    @property 
    def get_token(self):
        refresh = RefreshToken.for_user(self)
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}" 
    

class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_query_name="user", related_name="users_authentication_user_set")
    code = models.CharField(max_length=6, unique=True)
    
    def __str__(self):
        return f"{self.user.first_name}-passcode" 
