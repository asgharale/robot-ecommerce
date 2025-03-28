from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from phonenumber_field.modelfields import PhoneNumberField


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
        return self.is_admin
        
    def has_module_perms(self, app_label):
        return self.is_admin


class Address(models.Model):
    """Address model for users"""
    user = models.OneToOneField(CUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=500)
    house_number = models.CharField(max_length=5, blank=True)
    code = models.CharField(max_length=12)

    def __str__(self):
        return self.name