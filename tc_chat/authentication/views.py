from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from tc_chat.services.authentication import AuthService
from tc_chat.users.api.serializers import UserSerializer

from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """
    API endpoint that allows registering new users.
    """

    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": user_data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            access = response.data["access"]
            refresh = response.data["refresh"]
            user = AuthService().token_to_user(access)
            serializer = UserSerializer(user)
            data = {
                "access": access,
                "refresh": refresh,
                "user": serializer.data,
            }
            response.data = data
        return response
