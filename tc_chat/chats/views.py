from rest_framework import viewsets

from tc_chat.chats.models import ChatGroup
from tc_chat.chats.permissions import IsOwnerOrReadOnly
from tc_chat.chats.serializers import ChatGroupSerializer


class ChatGroupViewSet(viewsets.ModelViewSet):
    queryset = ChatGroup.objects.all()
    serializer_class = ChatGroupSerializer
    permission_classes = [IsOwnerOrReadOnly]
