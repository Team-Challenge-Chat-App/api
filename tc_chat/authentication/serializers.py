from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user with their username and password.

    Attributes:
        email: Should be unique
        username: Should be unique
        password
        name: optional
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())],
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data.get("name", ""),
        )

        user.set_password(validated_data["password"])
        user.save()

        return user

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "password", "email", "name")
        extra_kwargs = {"name": {"required": False}}
        read_only_fields = ["id"]
