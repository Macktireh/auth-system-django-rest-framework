from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .renderers import UserRenderer
from .tokens import get_tokens_for_user, generate_token
from .email import send_email_activation_account, send_email_activation_account_success
from . import serializers


User = get_user_model()

class UserSignupView(APIView):
    
    renderer_classes = [UserRenderer]
    
    def post(self, request, format=None):
        serializer = serializers.UserSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = generate_token.make_token(user)
            subject = "Confirmer votre adresse email de votre compte Mackdin"
            send_email_activation_account(get_current_site(request), user, token, subject, "account/activate.html")
            return Response(
                {'msg': "Inscription avec succès"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

def UserActivateAccountView(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None
    if user and generate_token.check_token(user, token):
        if not user.is_email_verified:
            user.is_email_verified = True
            user.save()
            subject = "Votre compte a été créé et activé avec succès !"
            send_email_activation_account_success(get_current_site(request), user, subject, 'account/activate_success.html')
        return redirect('https://mack-twitter.pages.dev/account/signin')
    return redirect('https://mack-twitter.pages.dev/not-found/')

class UserLoginView(APIView):
    
    renderer_classes = [UserRenderer]
    
    def post(self, request, format=None):
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                _user = User.objects.get(email=user.email)
                if _user.is_email_verified:
                    token = get_tokens_for_user(user)
                    return Response(
                        {'msg': "Connexion avec succès", "token": token},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {'error': "Veuillez d'abord confirmer votre adresse email"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'errors': "L'adresse email ou mot de passe incorrect"},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class UserProfilView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = serializers.UserProfilSerializer(request.user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = serializers.UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response(
                {'msg': "Mot de passe modifier avec succès"},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class SendEmailResetPasswordView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = serializers.SendEmailResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {'msg': "Le lien de réinitialisation du mot de passe a été envoyé. Veuillez vérifier votre email"},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class UserResetPasswordView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uidb64, token, format=None):
        serializer = serializers.UserResetPasswordSerializer(data=request.data, context={'uid': uidb64, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response(
                {'msg': "Mot de passe modifier avec succès"},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )