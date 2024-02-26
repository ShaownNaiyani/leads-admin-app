from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

# custom modules 
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email address"))
    first_name = models.CharField(max_length=50, verbose_name=_("First name"))
    last_name = models.CharField(max_length=50, verbose_name=_("Last name"))
    # permissions 
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(date_now_add=True)
    last_login = models.DateTimeField(date_now=True)
    
    # login username field 
    USERNAME_FIELD = "email"
    
    # required fields for registration and login
    REQUIRED_FIELDS = ["first_name", "last_name"]
    
    # user object manager 
    objects = UserManager()
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self) -> str:
        return f"{self.first_name}|{self.email}"
    


