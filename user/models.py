from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser

from user.managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(
        _("email address"),
        unique=True,

    )
    first_name = models.CharField(
        _("first name"),
        max_length=150
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150
    )
    last_request = models.DateTimeField(
        _("last request"),
        blank=True,
        null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
