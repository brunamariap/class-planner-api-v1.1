from django.db import models
from teacher.models import Teacher
from config import settings
class Course(models.Model):
    class Meta:
        db_table = 'course'

    name = models.CharField(max_length=100)
    degree = models.CharField(max_length=20)
    course_load = models.IntegerField()
    byname = models.CharField(max_length=10)  

    def __str__(self):
        return self.name

class Discipline(models.Model):
    class Meta:
        db_table = 'discipline'

    name = models.CharField(max_length=300)
    code = models.CharField(max_length=15, unique=True)
    workload_in_clock = models.IntegerField()
    workload_in_class = models.IntegerField()
    is_optional = models.BooleanField()
    courses = models.ManyToManyField(Course, related_name='course_disciplines', through='CourseDiscipline', through_fields=('discipline_id', 'course_id', 'period'))

    def __str__(self):
        return self.name
    

class CourseDiscipline(models.Model):
    class Meta:
        db_table = 'course_discipline'

    discipline_id = models.ForeignKey(Discipline, on_delete=models.CASCADE, db_column='discipline_id')
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='course_id')
    period = models.IntegerField(null=True, blank=True)


class Class(models.Model):
    class Meta:
        db_table = 'class'

    class Shift(models.TextChoices):
        MATUTINO = 'Manhã'
        VESPERTINO = 'Tarde'
        NOTURNO = 'Noite'
    
    class_leader_id = models.CharField(max_length=20, unique=True, null=True, blank=True, default=None)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='course_id')
    reference_period = models.IntegerField()
    shift = models.CharField(max_length=10, choices=Shift.choices)

    def __str__(self):
        return f'{self.course_id}, {self.reference_period}°, {self.shift}'

class Schedule(models.Model):
    class Meta:
        db_table = 'schedule'

    discipline_id = models.ForeignKey(Discipline, on_delete=models.CASCADE, db_column='discipline_id')
    quantity = models.IntegerField()
    weekday = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='class_id')

class ClassCanceled(models.Model):
    class Meta:
        db_table = 'class_canceled'

    class Status(models.TextChoices):
        PENDING = 'Pendente'
        REFUSED = 'Recusado'
        ACCEPTED = 'Aceito'

    schedule_id = models.ForeignKey(Schedule, on_delete=models.CASCADE, db_column='schedule_id')
    canceled_date = models.DateField()
    reason = models.TextField(max_length=200, blank=True, null=True)
    replace_class_status = models.CharField(max_length=10, choices=Status.choices, default='Pendente', blank=True)
    canceled_by = models.IntegerField()
    teacher_to_replace = models.ForeignKey(Teacher, db_column='teacher_to_replace', blank=True, on_delete=models.DO_NOTHING, null=True)

class Teach(models.Model):
    class Meta:
        db_table = 'teach'

    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, db_column='teacher_id')
    discipline_id = models.ForeignKey(Discipline, on_delete=models.CASCADE, db_column='discipline_id')
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='class_id')

class TemporaryClass(models.Model):
    class Meta:
        db_table = 'temporary_class'

    class_canceled_id = models.ForeignKey(ClassCanceled, on_delete=models.CASCADE, db_column='class_canceled_id')
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, db_column='teacher_id')
    discipline_id = models.ForeignKey(Discipline, on_delete=models.CASCADE, db_column='discipline_id')
