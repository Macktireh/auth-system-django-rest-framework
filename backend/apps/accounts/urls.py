
from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('me/', views.UserProfilView.as_view(), name='me'),
    path('activate-user/<uidb64>/<token>/', views.activate_user, name='activate'),
]