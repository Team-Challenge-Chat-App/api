from django.contrib.auth import get_user_model
from django.db.models import CASCADE
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import ForeignKey
from django.db.models import ManyToManyField
from django.db.models import Model

from tc_chat.custom_excpetions.chat_groups import CantDeleteDevGroupError
from tc_chat.custom_excpetions.chat_groups import GroupExcludesCreatorInMembersError


class ChatGroup(Model):
    name = CharField(max_length=100, unique=True)
    is_dev_created = BooleanField(
        help_text="Indicates if the group was created by developers", default=False
    )
    # Change the related_name to something unique, e.g., 'group_members'
    members = ManyToManyField(get_user_model(), related_name="chat_groups", blank=True)
    creator = ForeignKey(get_user_model(), on_delete=CASCADE, null=True, blank=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if creator is provided and not already in members
        if self.creator and self.creator not in self.members.all():
            raise GroupExcludesCreatorInMembersError
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Prevent deletion of developer-created groups."""
        if self.is_dev_created:
            raise CantDeleteDevGroupError
        super().delete(*args, **kwargs)

    def force_delete(self, *args, **kwargs):
        """
        Forces deletion of developer-created and other groups
        :param args:
        :param kwargs:
        :return:
        """
        super().delete(*args, **kwargs)
