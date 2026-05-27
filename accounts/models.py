from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("management", "Management"),
        ("operator", "Operator"),
        ("customer", "Customer"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")
    phone = models.CharField(max_length=30, blank=True, null=True)

    email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=10, blank=True, null=True)
    reset_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.username