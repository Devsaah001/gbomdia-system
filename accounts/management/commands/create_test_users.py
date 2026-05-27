from django.core.management.base import BaseCommand
from accounts.models import User
from customers.models import Customer


class Command(BaseCommand):
    help = "Create default GBOMDIA test users"

    def handle(self, *args, **kwargs):
        users = [
            {
                "username": "admin",
                "email": "admin@gbomdia.com",
                "password": "Admin12345",
                "first_name": "Admin",
                "last_name": "User",
                "role": "admin",
                "phone": "0888000001",
                "is_staff": True,
                "is_superuser": True,
                "email_verified": True,
            },
            {
                "username": "manager",
                "email": "manager@gbomdia.com",
                "password": "Manager12345",
                "first_name": "Management",
                "last_name": "User",
                "role": "management",
                "phone": "0888000002",
                "is_staff": False,
                "is_superuser": False,
                "email_verified": True,
            },
            {
                "username": "operator",
                "email": "operator@gbomdia.com",
                "password": "Operator12345",
                "first_name": "Operator",
                "last_name": "User",
                "role": "operator",
                "phone": "0888000003",
                "is_staff": False,
                "is_superuser": False,
                "email_verified": True,
            },
            {
                "username": "customer",
                "email": "customer@gbomdia.com",
                "password": "Customer12345",
                "first_name": "John",
                "last_name": "Smith",
                "role": "customer",
                "phone": "0888000004",
                "is_staff": False,
                "is_superuser": False,
                "email_verified": True,
            },
        ]

        for data in users:
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "email": data["email"],
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "role": data["role"],
                    "phone": data["phone"],
                    "is_staff": data["is_staff"],
                    "is_superuser": data["is_superuser"],
                    "email_verified": data["email_verified"],
                },
            )

            if created:
                user.set_password(data["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created {data['role']}: {data['username']}"))
            else:
                user.email = data["email"]
                user.first_name = data["first_name"]
                user.last_name = data["last_name"]
                user.role = data["role"]
                user.phone = data["phone"]
                user.is_staff = data["is_staff"]
                user.is_superuser = data["is_superuser"]
                user.email_verified = data["email_verified"]
                user.set_password(data["password"])
                user.save()
                self.stdout.write(self.style.WARNING(f"Updated {data['role']}: {data['username']}"))

            if data["role"] == "customer":
                Customer.objects.get_or_create(
                    phone=data["phone"],
                    defaults={
                        "first_name": data["first_name"],
                        "last_name": data["last_name"],
                        "email": data["email"],
                        "is_active": True,
                    },
                )

        self.stdout.write(self.style.SUCCESS("GBOMDIA test users ready."))