from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from tc_chat.chats.models import ChatGroup
from tc_chat.chats.permissions import IsOwnerOrReadOnly
from tc_chat.chats.serializers import ChatGroupSerializer
from tc_chat.custom_excpetions.chat_groups import GroupExcludesCreatorInMembersError


class ChatGroupViewSet(viewsets.ModelViewSet):
    queryset = ChatGroup.objects.all()
    serializer_class = ChatGroupSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def update(self, request, pk: int = None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.update(
                instance=instance, validated_data=serializer.validated_data
            )
        except GroupExcludesCreatorInMembersError as e:
            raise ValidationError("Group members should include a creator") from e
        return Response()
