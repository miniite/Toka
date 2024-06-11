from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth import get_user_model
from .models import CustomUser as User

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = User
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
