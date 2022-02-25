from django.contrib.auth import get_user_model


class PhoneAuthBackend:
    """
        Custom Authenticate with phone number
    """

    def authenticate(self, request, username=None, password=None):
        try:
            user = get_user_model().objects.get(phone_number=username)
            if user.check_password(password):
                return user
            return None
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
