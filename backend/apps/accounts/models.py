from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.managers import UserAccountManager


class UserAccount(AbstractUser):
    username = None
    email = models.EmailField(
        _('email address'), 
        unique=True,
        help_text=_("Required to authenticate")
    )
    is_email_verified = models.BooleanField(
        _('email verified'), 
        default=False,
        help_text=_("Specifies whether the user should verify their email address.")
    )
    last_logout = models.DateTimeField(
        _('last date logout'), 
        blank=True, null=True,
        help_text=_("last date logout user")
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserAccountManager()

    def __str__(self):
        return self.email
