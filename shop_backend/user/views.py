from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status,generics
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests
# from django_ratelimit.decorators import ratelimit
# from django_ratelimit.exceptions import Ratelimited
import os
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.

User=get_user_model()
from django.http import JsonResponse

def api_home(request):
    return JsonResponse({'message': 'Welcome to the API endpoint'})

#utility to generate tokens
def generate_tokens_for_user(user):
    refresh=RefreshToken.for_user(user)
    return{
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }



class RegisterView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response({
                "message":'User registered successfully',
                "user":{
                    "id":user.id,
                    "username":user.username,
                    "email":user.email,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def django_ratelimit_handler(request, exceptions):
#         return JsonResponse({'error':"Too many requests, Pls try again later"}, status=status.HTTP_429)



class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    # @ratelimit(key=lambda group, req: req.META.get('HTTP_X_FORWARDED_FOR', req.META.get('REMOTE_ADDR', '')), rate='5/m', block=True)
    # @ratelimit(key='ip', rate='5/m', block=True)

    def post(self, request, *args, **kwargs):
     
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            # if user.is_google_user:
            #     return Response({'error':'Google users must login with Google'}, status=status.HTTP_400_BAD_REQUEST)
            
            #Generate JWT tokens for normal user
            tokens = generate_tokens_for_user(user)
            return Response({'tokens':tokens,'username':user.username}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class GoogleLoginAPIView(APIView):
    # authentication_classes=[JWTAuthentication]
    permission_classes=[AllowAny]
    
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')

        if not token:
            return Response({'error':'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        #fetching Google client id
        client_id = os.getenv('GOOGLE_CLIENT_ID')  
        if not client_id:
            return Response({'error':'client id is not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
              

        try:
            idinfo=id_token.verify_oauth2_token(token, requests.Request(), client_id)
            #Extract user information from the token
            email = idinfo['email']
            name = idinfo.get('name','Unknown')

            #Check if the user with this email already exists in the database
            user, created =User.objects.get_or_create(
                email=email,
                defaults={'username':email.split('@')[0], 'first_name':name}
            )
            
            
      # Generate a JWT token for the authenticated user (optional)
            tokens = generate_tokens_for_user(user)

            if created:
                message = 'user created and logged in successfully'
            else:
                message = 'User logged in successfully'

            return Response({
                'message':message, 
                **tokens,
                'email':email,
                'name':name
            }, status=status.HTTP_200_OK)
        
        except ValueError as e:
            # Invalid token
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        try:
            refresh_token=request.data.get('refresh')
            token =RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout Successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'errro':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class UserListAPIView(generics.ListAPIView):
    queryset=User.objects.all()
    serializer=UserSerializer
    permission_classes=[AllowAny]


    # class GoogleLogin(SocialLoginView):
#     adapter_class=GoogleOAuth2Adapter
    
#     def post(self, request, *args, **kwargs):
#         response=super().post(request,*args, ** kwargs)   #call the parent class to handle auth logic
#         user=self.request.user      #the authenticated user who logged in via google

#     #generate jwt tokens
#         refresh =  RefreshToken.for_user(user)
#         jwt_tokens={
#             'refresh':str(refresh),
#             'access':str(refresh.access_token),
#         }
#         response.data.update(jwt_tokens)
#         return response

