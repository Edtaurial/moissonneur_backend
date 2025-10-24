import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create or update a Django superuser from environment variables if set.\n\n"

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")

        if not username or not password:
            self.stdout.write(self.style.WARNING(
                "DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD not set; skipping superuser creation/update."
            ))
            return

        User = get_user_model()
        user = User.objects.filter(username=username).first()
        if user:
            # Update existing user's password and flags
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            if email:
                user.email = email
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Updated superuser '{username}'."))
            return

        # Create new superuser
        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}'."))
