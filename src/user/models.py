from __future__ import annotations
from typing import Optional

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db.models import EmailField, BooleanField

from shared.models import UUIDModel


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: Optional[str] = None, **kwargs) -> User:
        if not email:
            raise ValueError("E-mail address is required")
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: Optional[str] = None, **kwargs) -> User:
        user = self.create_user(email=email, password=password, **kwargs)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, UUIDModel):
    class Fields(UUIDModel.Fields):
        PASSWORD = "password"
        LAST_LOGIN = "last_login"
        IS_ADMIN = "is_admin"
        IS_SUPERUSER = "is_superuser"
        EMAIL = "email"
        IS_ACTIVE = "is_active"
        PLATFORMS = "platforms"

    email = EmailField(max_length=255, unique=True)
    is_admin = BooleanField(default=False)
    is_active = BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = Fields.EMAIL

    def __str__(self) -> str:
        return self.email

    @property
    def is_staff(self) -> bool:
        return self.is_admin
