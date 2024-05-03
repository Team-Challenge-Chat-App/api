from django.urls import include
from django.urls import path

urlpatterns = [
    path("v1/authentication/", include("tc_chat.authentication.urls")),
    path("v1/chats/", include("tc_chat.chats.urls")),
    path("v1/", include("tc_chat.users.urls")),
]
