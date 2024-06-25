from rest_framework import permissions


""" Preciso de permissões que 
- Verifiquem se o professor que está tentando mudar uma aula é mesmo o "dono" da aula
- Se ele é professor ou funcionário da coades
- Se é aluno
- Se o aluno realmente faz parte da turma que ele está tentando dizer que não está tendo aula
"""


class IsTeacher(permissions.BasePermission):
    # def has_object_permission(self, request, view, obj):
    #     # Checo um objeto em si
    #     # return super().has_object_permission(request, view, obj)
    #     return obj.user == request.user

    def has_permission(self, request, view):
        # Posso estar checando qualquer coisa
        # Acho que é aqui
        # return super().has_permission(request, view)
        return request.user.department == 'Professor'


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Posso estar checando qualquer coisa
        # Acho que é aqui
        # return super().has_permission(request, view)

        # Correto
        # return request.user.department == 'COADES/PF'
        return request.user.department == 'Aluno'


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        # Posso estar checando qualquer coisa
        # Acho que é aqui
        # return super().has_permission(request, view)
        return request.user.department == 'Aluno'
