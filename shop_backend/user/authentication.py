# from django.contrib.auth.models import User
# from django.contrib.auth.backends import ModelBackend

# class EmailAuthBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             # Try to authenticate by email instead of username
#             user = User.objects.get(email=username)  # 'username' will be the email here
#             if user.check_password(password):
#                 return user
#         except User.DoesNotExist:
#             return None
