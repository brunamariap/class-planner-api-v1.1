from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action

from .serializers import UserSerializer

User = get_user_model()


class PersonViewset(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_queryset(self):
        User = get_user_model()
        # Retorna apenas o usuário logado
        queryset = User.objects.filter(
            registration=self.request.user.registration)
        return queryset

    @action(methods=['get'], detail=False)
    def me(self, request, *args, **kwargs):
        # Como eu estou tentando pegar o usuário logado, não tem como usar o get_object
        obj = self.get_queryset().first()
        serializer = self.get_serializer(
            instance=obj
        )

        return Response(serializer.data)
