"""
Database models.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=email, **extra_fields)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'


class LeadsData(models.Model):
    """store all fetched data"""
    asin = models.CharField(max_length=255, unique=True, verbose_name="ASIN")
    amazon_fba_estimated_fees = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="AmazonFBAEstimatedFees")
    amazon_price = models.DecimalField(max_digits=10, decimal_places=2)
    sourcing_price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_sales_rank = models.PositiveIntegerField(
        default=0, editable=False)
    sales_rank_30_days = models.PositiveIntegerField(default=0, editable=False)
    sales_rank_90_days = models.PositiveIntegerField(default=0, editable=False)
    estimated_monthly_sales = models.PositiveIntegerField(
        default=0, editable=False)
    product_image_url = models.URLField(blank=True)
    sourcing_url = models.URLField(blank=True)

    # product_image_url = models.URLField()
    # product_name = models.CharField(max_length=255)
    # amazon_fba_estimated_fees = models.DecimalField()
    # estimated_sales_rank = models.IntegerField(default=0, editable=False)
    # sales_rank_30_days = models.IntegerField(default=0, editable=False)
    # sales_rank_90_days = models.IntegerField(default=0, editable=False)
    # estimated_monthly_sales = models.IntegerField(default=0, editable=False)
    # amazon_price = models.DecimalField()
    # sourcing_url = models.URLField()
    # sourcing_price = models.DecimalField()
