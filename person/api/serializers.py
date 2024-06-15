from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

from ..models import Person
from utils.suap_api import SuapAPI

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'registration', 'name', 'email', 'department', 'avatar']
    # Sempre que um usuário fizer login é pra pegar a senha dele atualizada, então precisa ficar dando update em tudo


# Criar uma rota para login e na rota de login eu vejo se já existe algum usuário com aquela matrícula, se houver, eu só atualizo os dados, se não eu crio um
# Vejo se usuário passou pelo suap, se passou, pego os dados dele e mando pra o meu banco, mas antes disso verifico se o usuário com a matricula já existe, se existe, dou update

class RegisterUserSerializer(serializers.ModelSerializer):
    registration = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = [
            'registration',
            'password',
        ]

    def create(self, validated_data):
        registration = validated_data['registration']
        password = validated_data['password']

        suap_api = SuapAPI()
        user_data = suap_api.authenticate(registration, password)

        if user_data['success'] is True:
            user = User.objects.create_user(
                registration=registration,
                password=password,
                name=user_data['name'],
                department=user_data['department'],
                email=user_data['email'],
                avatar=user_data['picture'],
            )
            return user

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
