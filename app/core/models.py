"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
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
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Company(models.Model):
    """Company object."""
    name_company = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10, unique=True)
    cik = models.CharField(max_length=20, blank=True)
    sector = models.CharField(max_length=20, blank=True)
    industry_category = models.CharField(max_length=20, blank=True)
    company_url = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name_company

class FinancialIndicator(models.Model):
    """Financial indicators object."""
    description = models.TextField(blank=True)
    indicator_name = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.indicator_name
