from rest_framework import generics
from django.contrib.auth import get_user_model

from .serializers import RegisterUserSerializer
from utils.suap_api import SuapAPI


User = get_user_model()


class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        print(request)
        registration = request.data['registration']
        password = request.data['password']

        # suap_api = SuapAPI()
        # user_data = suap_api.authenticate(registration, password)
        return super().create(request, *args, **kwargs)
