from django.urls import include
from django.urls import path

urlpatterns = [
    path("v1/authentication/", include("tc_chat.authentication.urls")),
    path("v1/users/", include("tc_chat.users.urls"))
]
