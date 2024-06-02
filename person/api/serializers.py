from ..models import Person
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['registration', 'name', 'email', 'departament', 'avatar']


class RegisterUserSerializer(serializers.ModelSerializer):
    registration = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['registration', 'name', 'email', 'departament', 'avatar']

    def create(self, validated_data):
        user = User.objects.create_user(
            registration=validated_data['registration'],
            password=validated_data['password'],
            name=validated_data.get('name', ''),
            departament=validated_data.get('departament', ''),
            email=validated_data.get('email', '')
        )
        return user
