from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, LoginSerializer, CreateNewPasswordSerializer
from .models import MyUser
from .utils import send_activation_email


#TODO: register view


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Вы зарегестрированы!', status=status.HTTP_201_CREATED)
        return Response('Not Valid', status=status.HTTP_400_BAD_REQUEST)



#TODO: activate view
class ActivateView(APIView):
    def get(self, request, activation_code):
        User = get_user_model()
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('твой аккаунт успешно активирован', status=status.HTTP_200_OK)

#TODO: login view


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

#TODO: logout view


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('вы вышли', status=status.HTTP_200_OK)


class ForgotPassword(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        user = get_object_or_404(MyUser, email=email)
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_email(email=email, activation_code=user.activation_code, is_password=True)
        return Response('вам отправлен новый код на почту', status=status.HTTP_200_OK)


class ForgotPasswordComplete(APIView):
    def post(self, request):
        data = request.data
        serializer = CreateNewPasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Вы успешно восстановили пароль', status=status.HTTP_200_OK)
