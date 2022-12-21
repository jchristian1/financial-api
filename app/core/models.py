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
    cik = models.CharField(max_length=150, blank=True)
    sector = models.CharField(max_length=150, blank=True)
    industry_category = models.CharField(max_length=150, blank=True)
    company_url = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name_company


class Indicator(models.Model):
    """Financial indicators object."""
    description = models.TextField(blank=True)
    indicator_name = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.indicator_name


class Statement(models.Model):
    """Financial statement type object."""
    statement_name = models.CharField(max_length=150)

    def __str__(self):
        return self.statement_name


class StatementMetaData(models.Model):
    unique_hash = models.CharField(max_length=250, unique=True)
    id_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    id_statement_type = models.ForeignKey(
        Statement,
        on_delete=models.CASCADE, default=0
    )
    fiscal_year = models.CharField(max_length=50)
    fiscal_period = models.CharField(max_length=50)
    filling_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    url = models.CharField(max_length=150, blank=True)
    urlfinal = models.CharField(max_length=150, blank=True)
    unit = models.CharField(max_length=10)

    def __str__(self):
        return self.unique_hash
