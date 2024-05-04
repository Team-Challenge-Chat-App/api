from django.db import transaction
from rest_framework import serializers

from tc_chat.chats.models import ChatGroup
from tc_chat.custom_excpetions.chat_groups import GroupDoesntHaveCreatorError
from tc_chat.custom_excpetions.chat_groups import GroupExcludesCreatorInMembersError


class ChatGroupSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # Extract creator from validated data
        creator = validated_data.get("creator", None)
        # Extract members from validated data
        members = validated_data.pop("members", {})
        # Exclude duplications
        members = set(members)
        if creator:
            members.add(creator)
        # Create the chat group instance
        with transaction.atomic():
            # Create the chat group instance
            chat_group = ChatGroup(**validated_data)
            chat_group.save()
            # Add members to the chat group
            chat_group.members.set(members)
        return chat_group

    def update(self, instance, validated_data):
        creator = validated_data.get("creator")
        members = validated_data.get("members")
        if not creator:
            raise GroupDoesntHaveCreatorError
        if creator not in members:
            raise GroupExcludesCreatorInMembersError(
                message="Can't exclude creator from group members"
            )
        instance.name = validated_data.get("name")
        instance.members.set(members)
        instance.creator = creator
        instance.save()
        return instance

    class Meta:
        model = ChatGroup
        exclude = ["is_dev_created"]
        extra_kwargs = {"creator": {"required": True, "allow_null": False}}
