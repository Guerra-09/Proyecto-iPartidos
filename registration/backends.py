from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            print("User does not exist")  # Print statement for debugging
            return None

        if user.check_password(password):
            print("Password is correct")  # Print statement for debugging
            return user
        else:
            print("Password is incorrect")  # Print statement for debugging

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(pk=user_id)
            print("User found")  # Print statement for debugging
            return user
        except UserModel.DoesNotExist:
            print("User does not exist")  # Print statement for debugging
            return None