from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import UserProfilSerializer, UserSignupSerializer, UserLoginSerializer
from .renderers import UserRenderer
from .tokens import get_tokens_for_user, generate_token
from .email import send_email_activation_account, send_email_activation_account_success


User = get_user_model()

class UserSignupView(APIView):
    
    renderer_classes = [UserRenderer]
    
    def post(self, request, format=None):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_email_activation_account(request, user)
            return Response(
                {'msg': "Inscription avec succès"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class UserLoginView(APIView):
    
    renderer_classes = [UserRenderer]
    
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
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
        serializer = UserProfilSerializer(request.user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None
    if user and generate_token.check_token(user, token):
        if not user.is_email_verified:
            user.is_email_verified = True
            user.save()
            send_email_activation_account_success(request, user)
        return redirect('https://mack-twitter.pages.dev/account/signin')
    return redirect('https://mack-twitter.pages.dev/not-found/')