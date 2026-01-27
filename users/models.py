from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """

    display_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Custom display name (optional)")
    )

    @property
    def get_display_name(self):
        """
        Return the best available display name for the user.
        
        Falls back from display_name -> full name -> email username.
        """
        return self.display_name or self.get_full_name() or self.email.split('@')[0]

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
