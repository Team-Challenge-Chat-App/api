from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import EmailField
from django.db.models import Model
from django.db.models import BooleanField
from django.db.models import ManyToManyField
from django.db.models import CASCADE
from django.db.models import ForeignKey
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for Team Challenge Chat.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    username = CharField(_("username"), max_length=255, unique=True, null=True, default=None)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = EmailField(_("email address"), unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
    
class Group(Model):
    name = CharField(max_length=100, unique=True)
    is_dev_created = BooleanField(help_text="Indicates if the group was created by developers", default=False)
    # Change the related_name to something unique, e.g., 'group_members'
    members = ManyToManyField('User', related_name='group_members', blank=True)
    creator = ForeignKey('User', related_name='created_groups', on_delete=CASCADE, null=True, blank=True)

    def delete(self, *args, **kwargs):
        """Prevent deletion of developer-created groups."""
        if self.is_dev_created:
            return
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name
