from rest_framework import serializers
from ..models import Course, Discipline, Class, Schedule, Teach, CourseDiscipline


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'degree', 'course_load', 'byname']


class CourseDisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ['id', 'name', 'code', 'workload_in_clock', 'workload_in_class', 'is_optional']


class CourseDisciplinePeriodSerializer(serializers.ModelSerializer):
    #discipline = serializers.SerializerMethodField('show_discipline')
    discipline_id = CourseDisciplineSerializer(read_only=True)

    class Meta:
        model = CourseDiscipline
        fields = ['discipline_id', 'period']

    def show_discipline(self, instance):
        if instance:  
            discipline_obj = Discipline.objects.get(id=instance.discipline_id)
            print(discipline_obj)
            #discipline = CourseDisciplineSerializer(discipline_obj)
            #print(discipline)
            return {"discipline": discipline_obj}


class DisciplineSerializer(serializers.ModelSerializer):
    course_period = serializers.SerializerMethodField('show_course_period')

    class Meta:
        model = Discipline
        fields = ['id', 'name', 'code', 'workload_in_clock', 'workload_in_class', 'is_optional', 'course_period']

    def show_course_period(self, instance):
        course_discipline_objects = CourseDiscipline.objects.filter(discipline_id = instance.id)

        course_period = []
        for object in course_discipline_objects.values():
            course_period.extend([{'course_id':object['course_id_id'], 'period': object['period']}])

        return course_period


class TeachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teach
        fields = ['id', 'teacher_id', 'discipline_id', 'class_id']


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'course_id', 'reference_period', 'shift', 'class_leader']


class ScheduleSerializer(serializers.ModelSerializer):
    discipline = CourseSerializer(read_only=True)
    schedule_class = CourseSerializer(read_only=True)
    class Meta:
        model = Schedule
        fields = ['id', 'quantity', 'start_time', 'end_time', 'discipline', 'schedule_class']