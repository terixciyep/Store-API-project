from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise TypeError('Необходимо ввести почту')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise TypeError('Необходимо ввести почту')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class UserModel(AbstractUser):
    username = models.CharField(null=True,blank=True, max_length=255, unique=False)
    email = models.EmailField(unique=True)
    is_verify = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    object = UserManager()
