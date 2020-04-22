from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from shared.models import Supplier

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    ADMIN = 'ADMIN'
    STAFF = 'STAFF'
    MANAGEMENT = 'MANAGEMENT'
    SUPPLIER = 'SUPPLIER'

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (STAFF, 'Staff'),
        (MANAGEMENT, 'Management'),
        (SUPPLIER, 'Supplier')
    )

    PENDING = 'PENDING'
    ACTIVE = 'ACTIVE'
    DISABLED = 'DISABLED'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACTIVE, 'Active'),
        (DISABLED, 'Disabled')
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    email = models.EmailField('email address', unique=True)
    phone_number = PhoneNumberField(null=True, unique=True)
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    role = models.ForeignKey(
        Group,
        blank=True, null=True,
        on_delete=models.SET_NULL
    )
    supplier = models.ForeignKey(
        Supplier,
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = CustomUserManager()

    class Meta(AbstractUser.Meta):
        default_related_name = 'users'

    def __str__(self):
        return self.email
