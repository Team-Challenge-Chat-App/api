from logging import getLogger

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

logger = getLogger(__name__)


class AuthService:
    """
    Service class for handling authentication related operations.
    """

    def header_to_user(self, headers):
        """
        Extracts the user from the JWT token obtained from the request headers.
        :param headers: Dictionary containing request headers.
        :return: The user object if authentication is successful, None otherwise.
        """
        try:
            auth_header = headers.get(b"authorization", b"").decode("utf-8")
            jwt_token = auth_header.split()[1]
            return self.token_to_user(jwt_token)
        except Exception as e:
            logger.exception("JWT Auth header to user failed", exc_info=e)
            return None

    def token_to_user(self, token):
        try:
            access_token = AccessToken(token)
            user_payload = access_token.payload
            _id = user_payload.get("user_id")
            return get_user_model().objects.get(pk=_id)
        except Exception:
            logger.exception(
                "Broad exception occured on JWT token to user!", exc_info=Exception
            )
