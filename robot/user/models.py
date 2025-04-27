from datetime import timedelta
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber
import django_jalali.db.models as jmodels
import uuid
import random
import string
from .sender import send_otp
from django.utils import timezone
from django.core.exceptions import ValidationError


def generate_otp():
    rand = random.SystemRandom()
    digits = rand.choices(string.digits, k=4)
    return ''.join(digits)


class CUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password=None):
        if not password:
            raise ValueError("PLEASE ENTER A PASSWORD")
        if not username:
            raise ValueError("Users must have a phone number")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, password=None):
        user = self.create_user(
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CUserAdminManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)


class OTPRequestQuerySet(models.QuerySet):
    def is_valid(self, receiver, request_id, password):
        current_time = timezone.now()
        return self.filter(
            receiver=receiver,
            request_id=request_id,
            password=password,
            created__lt=current_time,
            created__gt=current_time-timedelta(seconds=120),
        ).exists()


class OTPManager(models.Manager):
    def get_queryset(self):
        return OTPRequestQuerySet(self.model, self._db)

    def is_valid(self, receiver, request_id, password):
        return self.get_queryset().is_valid(
            receiver=receiver,
            request_id=request_id,
            password=password
        )

    def generate(self, data):
        otp = self.model(receiver=data['receiver'], password=generate_otp())
        otp.save(using=self._db)
        send_otp(otp)
        return otp


class CUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""
    username = PhoneNumberField(unique=True, region='IR')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthdate = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    # relations
    favorates = models.ManyToManyField("products.Product")

    # custom user manager
    objects = CUserManager()
    admins = CUserAdminManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return str(self.username)
    
    class Meta:
        ordering = ('id',)
        
    def has_perm(self, perm, obj=None):
        if self.is_admin:
            return True
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        if self.is_admin:
            return True
        return super().has_module_perms(app_label)


class Address(models.Model):
    """Address model for users"""
    user = models.OneToOneField(CUser, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=500)
    house_number = models.CharField(max_length=5, blank=True)
    code = models.CharField(max_length=12)

    def __str__(self):
        return self.name


class OTPRequest(models.Model):
    request_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    receiver = PhoneNumberField(region='IR')
    password = models.CharField(max_length=4, default=generate_otp())
    created = models.DateTimeField(auto_now_add=True, editable=False)

    objects = OTPManager()

    def __str__(self):
        return str(self.request_id)