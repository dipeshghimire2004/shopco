from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials. Please try again.")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']




# Serializer for user login
# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()  # email field
#     password = serializers.CharField(write_only=True)  # Password field (write-only)


#     def validate(self, data):
#         user =authenticate(username=data['email'], password=data['password'])

#         if user and user.is_active:
#             return user 
#         raise serializers.ValidationError("Tnvalid Credentials")






    # access = serializers.CharField(read_only=True)  # Access token (read-only)
    # refresh = serializers.CharField(read_only=True)  # Refresh token (read-only)
    # user = serializers.SerializerMethodField()  # User data field

    # def validate(self, data):
    #     # Extract username and password from the input data
    #     email = data.get('email')
    #     password = data.get('password')

    #     # Ensure both fields are provided
    #     if not email or not password:
    #         raise serializers.ValidationError("Username and password are required.")

    #     # Authenticate the user
    #     user = authenticate(emial=email, password=password)
    #     if not user or not user.is_active:
    #         # Raise an error if the user doesn't exist or is inactive
    #         raise serializers.ValidationError("Invalid username or password.")

    #     # Generate JWT tokens for the authenticated user
    #     refresh = RefreshToken.for_user(user)
    #     return {
    #         'refresh': str(refresh),  # Return the refresh token
    #         'access': str(refresh.access_token),  # Return the access token
    #         'user': {
    #             "id": user.id,  # Include user ID
    #             "username": user.username,  # Include username
    #             "email": user.email,  # Include email
    #         },
    #     }

    # def get_user(self, obj):
    #     # Method to retrieve the user object (redundant here, but kept for compatibility)
    #     return obj.get('user')
    