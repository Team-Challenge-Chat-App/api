from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db.models import CharField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from tc_chat.users.managers import UserManager

EMAIL_MIN_LENGTH = 30


class User(AbstractUser):
    """
    Default custom user model for Team Challenge Chat.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    username = CharField(_("username"), max_length=64, unique=True, default=None)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = EmailField(
        _("email address"),
        unique=True,
        validators=[
            MinLengthValidator(
                EMAIL_MIN_LENGTH,
                f"the field must contain at least {EMAIL_MIN_LENGTH} characters",
            )
        ],
        max_length=255,
        default=None,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
