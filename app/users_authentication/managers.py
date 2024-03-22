from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Some words from SHAMIM:
    The main job of UserManager is to create user and superuser by using necessary method, 
    attribute and property from BaseUserManager class
    """
    # validate whether the email is already registered
    def email_validators(self, email: str) -> str:
        try:
            validate_email(email) 
        except ValidationError:
            raise ValidationError("Please enter valid email address!")
        else:
            return email  
    
    def create_user(self, email, password, first_name, last_name, **extra_fields):
        if email:
            ''' 
            Some words from SHAMIM:
            Normalize email to prevent using the same email domain 
            with different uppercase lowercase combination
            abc@Naiyani.com, abc@naYani.com, abc@naiyani.COM 
            will be abc@naiyani.com
            '''
            email = self.normalize_email(email)
            email = self.email_validators(email) 
        else:
            raise ValueError("Email address is required!") 
        
        # create user using User model 
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        # set the password using set_password method from BaseUserManager
        # set_password() function will take care all necessary encryption, hashing etc
        user.set_password(password)
        # save the user in the default authentication database
        # you have to set your custom auth user model in the settings file 
        # custom auth_user_model 
        # AUTH_USER_MODEL = "users_authentication.User"
        user.save(using=self._db)
        
        return user 

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault("is_staff", True) 
        extra_fields.setdefault("is_superuser", True) 
        extra_fields.setdefault("is_verified", True) 
        
        if not extra_fields.get("is_staff"):
            raise ValidationError("is staff must be true for admin user!")
        
        if not extra_fields.get("is_superuser"):
            raise ValidationError("is superuser must be true for admin user!")
        
        if not extra_fields.get("is_verified"):
            raise ValidationError("is verified must be true for admin user!")
        
        user = self.create_user(self, email, first_name, last_name, password, **extra_fields)
        return user 