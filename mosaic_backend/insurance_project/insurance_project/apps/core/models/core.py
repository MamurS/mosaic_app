import uuid
from typing import Any, Dict, Optional

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_%(class)ss',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='updated_%(class)ss',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def soft_delete(self) -> None:
        self.is_active = False
        self.save(update_fields=['is_active'])


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: Optional[str], **extra_fields: Any):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: Optional[str] = None, **extra_fields: Any):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields: Any):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)

    # Domain-specific fields
    role = models.CharField(max_length=50, blank=True)
    org_unit = models.CharField(max_length=100, blank=True)
    underwriting_authority = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    claims_authority = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    phone = models.CharField(max_length=32, blank=True)
    locale = models.CharField(max_length=32, default='ru-RU')
    timezone = models.CharField(max_length=64, default='Asia/Tashkent')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    class Meta:
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self) -> str:
        return self.email


class Currency(BaseModel):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=8, blank=True)

    class Meta:
        verbose_name_plural = 'Currencies'
        indexes = [models.Index(fields=['code'])]

    def __str__(self) -> str:
        return self.code


class Country(BaseModel):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = 'Countries'
        indexes = [models.Index(fields=['code']), models.Index(fields=['name'])]

    def __str__(self) -> str:
        return self.name


class Industry(BaseModel):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self) -> str:
        return self.name


class SystemSetting(BaseModel):
    key = models.CharField(max_length=128, unique=True)
    value = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.key


class AuditLog(BaseModel):
    EVENT_TYPES = (
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('action', 'Action'),
    )

    event_type = models.CharField(max_length=32, choices=EVENT_TYPES)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    payload = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']


def write_audit_event(event_type: str, actor: Optional[User], payload: Optional[Dict[str, Any]] = None) -> AuditLog:
    return AuditLog.objects.create(event_type=event_type, actor=actor, payload=payload or {})


