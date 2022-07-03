from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    
    # Nous écrivons ceci parce que nous avons besoin d'un champ de confirmation de mot de passe dans notre demande d'enregistrement.
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = [
            'email',
            'name',
            'tc',
            'password',
            'password2',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    # Validation du mot de passe et confirmation du mot de passe lors de l'enregistrement
    def validate(self, attrs):

        email = attrs.get('email')
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "L'utilisateur avec cette adresse e-mail existe déjà."
            )
        if password != password2:
            raise serializers.ValidationError(
                "Le mot de passe et le mot de passe de confirmation ne correspondent pas."
            )
        return super().validate(attrs)

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


# User Serializer Login
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ]



# User Serializer Login
class UserProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'name',
        ]