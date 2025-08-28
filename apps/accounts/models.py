from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class _UserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Meta:
        verbose_name = _('Utilisateur')
        verbose_name_plural = _('Utilisateurs')
        ordering = ['first_name', 'last_name', ]

    username = None
    email = models.EmailField(_("Email"), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = _UserManager()

    def delete(self, **kwargs):
        self.is_active = False
        self.save(update_fields=['is_active'])
        return self

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
