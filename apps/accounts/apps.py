from django.apps import AppConfig
from django.core.management import call_command
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = _('Compte Utilisateur')

    def ready(self):
        from .spectacular_extensions import JWTAndCookieAuthenticationScheme
        setattr(self, 'scheme', JWTAndCookieAuthenticationScheme)

        post_migrate.connect(self.create_default_admin, sender=self)

    def create_default_admin(self, *args, **kwargs):
        call_command('create_default_admin')
