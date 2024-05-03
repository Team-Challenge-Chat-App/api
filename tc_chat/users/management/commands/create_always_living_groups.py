from django.core.management.base import BaseCommand

from tc_chat.users.models import Group
from tc_chat.users.models import User


def create_always_living_groups():
    """Create mock data for development purposes."""

    # Create users
    user_data = [
        {
            "username": "alice",
            "email": "alice@example.com",
            "password": "securepassword123",
            "groups": ["IT", "Cooking"],
        },
        {
            "username": "bob",
            "email": "bob@example.com",
            "password": "securepassword123",
            "groups": ["Sport"],
        },
        {
            "username": "carol",
            "email": "carol@example.com",
            "password": "securepassword123",
            "groups": ["Cooking", "Sport"],
        },
    ]

    users = {}
    for user_info in user_data:
        user, created = User.objects.get_or_create(
            username=user_info["username"],
            email=user_info["email"],
            defaults={"is_staff": False, "is_superuser": False},
        )
        if created:
            user.set_password(user_info["password"])
            user.save()
        users[user_info["username"]] = user

    # Create groups and assign a creator and members
    group_names = ["IT", "Cooking", "Sport"]
    groups = {}

    for name in group_names:
        # Fetch a random user as the creator; for simplicity using the first user
        creator = users["alice"]  # Example to set 'alice' as creator of all groups
        group, created = Group.objects.get_or_create(
            name=name, defaults={"is_dev_created": True, "creator": creator}
        )
        if created:
            for user_info in user_data:  # Add members who should be in this group
                if name in user_info["groups"]:
                    group.members.add(users[user_info["username"]])
        groups[name] = group


class Command(BaseCommand):
    help = "Create always living developers group"

    def handle(self, *args, **kwargs):
        create_always_living_groups()
        self.stdout.write(self.style.SUCCESS("Mock data created successfully"))
