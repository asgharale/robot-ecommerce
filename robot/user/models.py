from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField


class CUserManager(BaseUserManager):
	def create_user(self, email, phonenumber, first_name, last_name, password=None):
		if not email:
			raise ValueError("Users must have an email address")
		if not password:
			raise ValueError("PLEASE ENTER AN phonenumber")
		if not phonenumber:
			raise ValueError("Users must have an phone number")
		if not first_name:
			raise ValueError("Users must have a first name")
		if not last_name:
			raise ValueError("Users must have a last name")

		user = self.model(
			email=self.normalize_email(email),
			username=phonenumber,
			first_name=first_name,
			last_name=last_name
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, phonenumber, first_name, last_name, password=None):
		user = self.create_user(
			email,
			password=password,
			username=phonenumber,
			first_name=first_name,
			last_name=last_name
		)
		user.is_admin = True
		user.save(using=self._db)
		return user

class CUserAdminManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(is_admin=True)



class CUser(AbstractBaseUser, PermissionsMixin):
	"""Custom user model."""
	phonenumber = PhoneNumberField(unique=True, region='IR', max_length=13)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	birthdate = models.DateField(blank=True)
	email = models.EmailField(max_length=255, blank=True, unique=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	phone_verified = models.BooleanField(default=False)
	email_verified = models.BooleanField(default=False)

	# custom user manager
	objects = CUserManager()
	admins = CUserAdminManager()

	USERNAME_FIELD = 'phonenumber'
	REQUIRED_FIELDS = ['first_name', 'last_name']

	@property
	def is_staff(self):
		return self.is_admin

	def __str__(self):
		return self.username
	class Meta:
		ordering = ('id',)
	def has_perm(self, perm: str, obj=None):
		return self.is_admin
	def has_module_perms(self, app_label: str):
		return self.is_admin
