from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy

from users.models import UserModel
from users.serializers import UserModelSerializer
from users.signals import create_profile
from users.utils import send_mail_for_verify


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer

    @swagger_auto_schema(
        operation_summary="Create user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],  # Указываем обязательные поля
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING,title='Почта', description='Ввод почты'),
                'password': openapi.Schema(type=openapi.TYPE_STRING,title='Пароль', description='Ввод пароля'),
            }
        ),
        responses={201: openapi.Response('Пользователь создаг', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "password": openapi.Schema(type=openapi.TYPE_STRING),
                    "last_login": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                    "is_superuser": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                    "last_name": openapi.Schema(type=openapi.TYPE_STRING),
                    "is_staff": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    "date_joined": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                    "username": openapi.Schema(type=openapi.TYPE_STRING),
                    "email": openapi.Schema(type=openapi.TYPE_STRING),
                    "is_verify": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    "groups": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
                    "user_permissions": openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            }))},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        post_save.connect(create_profile, sender=UserModel)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ActivateAccount(GenericAPIView):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and default_token_generator.check_token(user, token):
            user.is_verify = True
            user.save()
            login(request, user)
            return redirect(reverse_lazy('schema-swagger-ui'))
        return redirect('schema-swagger-ui')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                UserModel.DoesNotExist, ValidationError):
            user = None
        return user
