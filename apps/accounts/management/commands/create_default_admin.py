from django.conf import settings
from django.core.management import BaseCommand

from apps.accounts.models import User


class Command(BaseCommand):
    help = 'Create admin user'

    requires_migrations_checks = True

    def handle(self, *args, **options):
        if not settings.DEBUG:
            self.stdout.write(self.style.ERROR('This command can only be used in debug mode'))
            return

        user, created = User.objects.get_or_create(
            email='admin@localhost',
            defaults={
                'first_name': '',
                'last_name': '',
            }
        )
        if created:
            user.is_staff = True
            user.is_superuser = True
            user.set_password('admin')
            user.save()
            self.stdout.write(self.style.SUCCESS('Admin user created successfully'))
        else:
            self.stdout.write(self.style.NOTICE('Admin user already exists'))
