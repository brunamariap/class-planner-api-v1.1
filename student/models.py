from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from course.models import Class, Discipline, Teacher


User = get_user_model()


class Student(models.Model):
    class Meta:
        db_table = 'student'

    registration = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=200)
    avatar = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=254)
    class_id = models.ForeignKey(
        Class, on_delete=models.CASCADE, db_column='class_id')
    disciplines = models.ManyToManyField(Discipline)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        return super().save(force_insert, force_update, using, update_fields)

    # Pode ser uma relação one to one, que um estudante só pode ser criado se o tipo do vínculo for estudante, quando o vinculo for estudante é pra disparar um signal pra cria um estudante

    def __str__(self) -> str:
        return f'{self.registration} - {self.name}'


""" 
class StudentDisciplines(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='student_id')
    discipline_id = models.ForeignKey(Discipline, on_delete=models.CASCADE, db_column='discipline_id') 
"""


class StudentAlert(models.Model):
    class Meta:
        db_table = 'student_alert'

    discipline_id = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        db_column='discipline_id'
    )

    student_id = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        db_column='student_id',
        related_name='students'
    )

    teacher_id = models.ForeignKey(
        User, on_delete=models.CASCADE,
        db_column='teacher_id',
        related_name='teachers'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    reason = models.TextField(
        max_length=200,
        blank=True,
        null=True,
        default=None
    )
