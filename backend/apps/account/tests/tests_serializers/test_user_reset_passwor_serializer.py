from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.account import serializers

User = get_user_model()

class UserResetPasswordSerializerTests(TestCase):

    def setUp(self):
        self.user_attributes = {
            'first_name': 'Mack',
            'last_name': 'AS',
            'email': 'mack@gmail.com',
            'password': '12345',
        }
        self.serializer_data = {
            'password': '12345',
            'password2': '12345',
        }
        self.user  = User.objects.create(**self.user_attributes)