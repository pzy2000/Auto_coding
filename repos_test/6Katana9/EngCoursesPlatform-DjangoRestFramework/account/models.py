from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

class Level(models.Model):
    title = models.CharField(max_length=100, default='notlevel')

    def __str__(self) -> str:
        return self.title

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        if not email: raise ValueError('email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email: raise ValueError('email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    password = models.CharField(max_length=100)
    is_active = models.BooleanField("active", default=False)

    activation_code = models.CharField(max_length=36, blank=True)
    objects = UserManager()

    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField('email address', unique=True)
    full_name = models.CharField(max_length=100)

    level = models.ForeignKey(Level, default=1, on_delete=models.SET_DEFAULT, related_name='students', null=True, blank=True)
    status = models.CharField(max_length=100)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['level']

    def __str__(self):
        return self.email

    def create_activation_code(self):
        import hashlib
        string_to_encode = self.email
        encode_string = string_to_encode.encode()
        md5_object = hashlib.md5(encode_string)
        activations_code = md5_object.hexdigest()
        self.activation_code = activations_code

