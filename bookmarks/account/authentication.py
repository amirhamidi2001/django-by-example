from django.contrib.auth.models import User

from account.models import Profile


class EmailAuthBackend:
    """
    Custom Authentication Backend for Django.
    """

    def authenticate(self, request, username=None, password=None):
        """
        Verifies credentials based on email and password.
        """
        try:
            user = User.objects.get(email__iexact=username)
            if user.check_password(password):
                return user
            return None

        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        """
        Retrieves a User instance from a user ID.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def create_profile(backend, user, *args, **kwargs):
    """Automatically create a profile when a new user is created."""
    Profile.objects.get_or_create(user=user)
