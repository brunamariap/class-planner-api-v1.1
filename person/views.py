import requests
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class SuapAPIAuth(APIView):
    def post(self, request):
        self.token = None
        self.endpoint = 'https://suap.ifrn.edu.br/api/v2/'

        username = self.request.data.get('registration')
        self.password = self.request.data.get('password')

        data = self.authenticate(username, self.password)

        if isinstance(data, User):
            refresh = RefreshToken.for_user(data)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(data)

    def authenticate(self, username, password):
        url = self.endpoint+'autenticacao/token/'
        params = {
            'username': username,
            'password': password,
        }

        response = requests.post(url, data=params)
        data = {
            'success': False,
            'message': "Usuário e/ou senha incorreto(s). Tente novamente"
        }

        if response.status_code == 200:
            data = response.json()
            data['success'] = True
            self.set_token(data['access'])
            self.set_token_refresh(data['refresh'])
            data = self.get_user_data(data['access'])
        else:
            data['message'] = response.json()['detail']
        return data

    def set_token(self, token):
        self.token = token

    def set_token_refresh(self, refresh_token):
        self.refresh_token = refresh_token

    def get_refresh_token(self):
        url = self.endpoint+'autenticacao/token/refresh/'
        params = {
            'refresh': self.refresh_token
        }
        response = requests.post(url, data=params)
        if response.status_code == 200:
            data = response.json()
            self.set_token(data)
        else:
            print("(!) Não foi possível atualizar o token", response.status_code)

    def get_request(self, url, token):
        response = requests.get(
            url, headers={'Authorization': f'Bearer {token}'})
        data = False
        if response.status_code == 200:
            data = response.json()
        return data

    def get_user_data(self, token):
        url = self.endpoint+'minhas-informacoes/meus-dados/'
        response = self.get_request(url, token)

        error = {
            'message': 'Você não tem permissão para acessar o sistema.',
            'success': False
        }

        if response is not False:
            user, created = User.objects.get_or_create(
                registration=response['matricula'])

            # if not created:
            user.name = response['nome_usual']
            user.email = response['email']
            user.avatar = response['url_foto_75x100']
            user.department = response['tipo_vinculo']

            # Estudante response['vinculo']['curso']

            user.set_password(self.password)
            user.save()

            return user

            # if 'setor_suap' in response['vinculo'] and (response['vinculo']['setor_suap'] == 'COAPAC/PF' or response['vinculo']['setor_suap'] == 'COADES/PF'):
            #     return data

            return data  # Devia ser error, mas não está em produção

        return error
