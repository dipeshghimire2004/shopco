from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField( max_length=50, unique=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return self.email
    # Add your custom fields here
    # Example:
    # birthdate = models.DateField(null=True, blank=True)
    
    # is_google_user = models.BooleanField(default=False)
    # profile_picture = models.URLField(unique=True)

    # Customizing the related_name for 'groups' and 'user_permissions' to avoid clashes
    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     related_name='customuser_set',  # Changed related_name
    #     blank=True,
    #     help_text='The groups this user belongs to.',
    #     related_query_name='customuser',
    # )

    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     related_name='customuser_set',  # Changed related_name
    #     blank=True,
    #     help_text='Specific permissions for this user.',
    #     related_query_name='customuser',
    # )
