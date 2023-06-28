from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework.exceptions import NotFound
import json
from django.contrib import messages
from django.shortcuts import render, redirect
from rest_framework.decorators import action
from django.urls import reverse
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from . import serializers, services, repos, permissions, models
from users.tokens import account_activation_token

auth_services = services.AuthServices()
profile_services = services.ProfileServices()


class RegisterView(APIView):
    repos = repos.AuthRepos()

    @swagger_auto_schema(method='POST', request_body=serializers.CreateUserSerializer())
    @action(detail=False, methods=['POST'])
    def post(self, request, *args, **kwargs):
        serializer = serializers.CreateUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswordView(APIView):
    repos = repos.AuthRepos()
    services = services.AuthServices()
    # permission_classes = [permissions.IsActiveUserPermission]

    @swagger_auto_schema(
        method='PUT',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'password1': openapi.Schema(type=openapi.TYPE_STRING),
                'password2': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['password1', 'password2']
        )
    )
    @action(detail=False, methods=['PUT'])
    def put(self, request, user_id):
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')

        validated_result = auth_services.validate_passwords(password1, password2)
        if validated_result == password1:
            # Update the user's password
            self.services.update_password(user_id=user_id, new_password=password1)

            return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)

        return Response(validated_result, status=status.HTTP_400_BAD_REQUEST)


class ProfileForm(APIView):
    model = models.Profile
    repos = repos.ProfileRepos()
    permission_classes = [permissions.IsAuthorizedPermission]

    @swagger_auto_schema(method='PUT', request_body=serializers.UpdateProfileSerializer())
    @action(detail=False, methods=['PUT'])
    def put(self, request):
        profile = self.repos.get_profile(user_id=request.user.id)
        serializer = serializers.UpdateProfileSerializer(profile, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: serializers.RetrieveProfileSerializer()})
    def get(self, request, *args, **kwargs):
        try:
            profile = self.repos.get_profile(user_id=request.user.id)
        except self.model.DoesNotExist:
            return Response({"detail": "Вы еще не создали профиль."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.RetrieveProfileSerializer(profile)

        return Response(serializer.data)


class UpdatePhoneNumberView(APIView):
    """
    Send SMS to phone number for verification.
    """
    user_model = models.User
    repos = repos.ProfileRepos()
    permission_classes = [permissions.IsAuthorizedPermission]

    @swagger_auto_schema(method='POST', request_body=serializers.UpdatePhoneNumberSerializer())
    @action(detail=False, methods=['POST'])
    def post(self, request):
        serializer = serializers.UpdatePhoneNumberSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhoneNumberVerificationView(APIView):
    """
    Check verification code sent to phone number
    """
    permission_classes = [permissions.IsAuthorizedPermission]

    @swagger_auto_schema(method='POST', request_body=serializers.VerifyCodeSerializer())
    @action(detail=False, methods=['POST'])
    def post(self, request, phone_number):
        context = {
            'phone_number': phone_number,
            'user_id': request.user.id
        }
        serializer = serializers.VerifyCodeSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    repos = repos.AuthRepos()
    services = services.AuthServices()

    @swagger_auto_schema(request_body=serializers.LoginSerializer())
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Perform authentication logic
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Authentication succeeded
                login(request, user)  # Log the user in

                # Generate or retrieve the user's authentication token
                token = self.create_token(request)

                # Return the token and any other necessary data in the response
                data = {
                    'token': token,
                    'user_id': user.id,
                    'username': user.username,
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                # Authentication failed
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_token(self, request):
        serializer = serializers.LoginSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        tokens = self.services.create_token(data=serializer.validated_data)
        return tokens


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthorizedPermission]

    def post(self, request):
        try:
            logout(request)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
