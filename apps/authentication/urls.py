from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from drf_yasg.utils import swagger_auto_schema

from apps.authentication import views
from apps.utils import postCreate


decorated_TokenRefreshView = swagger_auto_schema(
    method='post',
    tags=['Auth'],
)(TokenRefreshView.as_view())


urlpatterns = [
    path('signup/', views.SignupView.as_view(postCreate), name='signup'),
    path('account/activation/', views.ActivationView.as_view(postCreate), name='activate'),
    path('login/', views.LoginView.as_view(postCreate), name='login'),
    path('change-password/', views.UserChangePasswordView.as_view(postCreate), name='change_password'),
    path('request/reset-password/', views.RequestResetPasswordView.as_view(postCreate), name='reset_password_send_email'),
    path('reset-password/<uidb64>/<token>/', views.UserResetPasswordView.as_view(postCreate), name='reset_password'),
    path('token/refresh/', decorated_TokenRefreshView, name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='verify_jwt'),
    path('logout/', views.LogoutView.as_view(postCreate), name='logout'),
]