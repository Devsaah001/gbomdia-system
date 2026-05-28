from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = "Create production super admin"

    def handle(self, *args, **kwargs):
        username = "saahfrancistamba"
        email = "support@gbomdia.com"
        password = "Treasure28@2026.($&)"

        user, created = User.objects.get_or_create(username=username)

        user.email = email
        user.role = "admin"
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.email_verified = True
        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS("Super admin created successfully."))