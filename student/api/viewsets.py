import copy
from datetime import date, datetime, timedelta

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from course.api.serializers import DisciplineWithTeachSerializer  # noqa E051
from course.api.serializers import ScheduleSerializer
from course.models import (
    Class,
    ClassCanceled,
    Course,
    CourseDiscipline,
    Discipline,
    Schedule,
    TemporaryClass,
)
from utils.generate_month_days import get_days_from_month
from utils.suap_api import SuapAPI

from ..models import Student, StudentAlert
from .serializers import (
    CreateStudentSerializer,
    StudentAlertSerializer,
    StudentSerializer,
)

User = get_user_model()


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def create(self, request):
        data = request.data
        student_disciplines = data["disciplines"]
        student_course = data["course"]
        student_class_shift = data["shift"]
        suap_api = SuapAPI()
        response = suap_api.authenticate(
            data["registration"],
            data["password"],
        )

        if response["success"] is not False:
            user = User.objects.create(
                registration=response["registration"],
                name=response["name"],
                avatar=response["avatar"],
                department=response["department"],
                email=response["email"],
            )
            user.set_password(data["password"])
            user.save()

            disciplines = Discipline.objects.filter(
                code__in=student_disciplines,
            )
            # O nome do curso cadastrado precisa ser igual ao do cadastrado no SUAP para que funcione
            course = Course.objects.get(name=student_course)

            relation = CourseDiscipline.objects.filter(
                discipline_id__in=disciplines, course_id=course.id
            )

            period = None
            for course_discipline in relation.values():
                currentPeriod = course_discipline["period"]

                if period is None:
                    period = currentPeriod
                elif currentPeriod is not None and currentPeriod < period:
                    period = currentPeriod

            student_class = Class.objects.get(
                course_id=course,
                reference_period=period,
                shift=student_class_shift,
            )

            request.data["class_id"] = student_class.id
            request.data["user"] = user

            serializer = CreateStudentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )

        return Response(
            {"message": "Usuário e/ou senha incorretos"},
            status=status.HTTP_401_UNAUTHORIZED,
            headers=headers,
        )

    @action(
        methods=["GET"],
        detail=False,
        url_path="byregistration/(?P<student_registration>[^/.]+)",
        # permission_classes=[IsAuthenticated],
    )
    def get_student_by_registration(self, request, student_registration):
        try:
            student = Student.objects.get(registration=student_registration)

            serializer = StudentSerializer(student)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"data": None, "details": "Não encontrado"},
                status=status.HTTP_200_OK,
            )

    @action(
        methods=["GET"],
        detail=False,
        url_path="(?P<student_id>[^/.]+)/schedules/week",
        # permission_classes=[IsAuthenticated]
    )
    def get_week_schedules(self, request, student_id):
        student = Student.objects.get(id=student_id)
        student_values = StudentSerializer(student)
        student_disciplines = Discipline.objects.filter(
            code__in=student_values.data["disciplines"]
        ).values_list("code", flat=True)

        disciplines = Discipline.objects.filter(
            id__in=student.disciplines.values_list("id", flat=True)
        )
        classes = Class.objects.filter(
            course_id=student.class_id.course_id, shift=student.class_id.shift
        )
        schedules = Schedule.objects.filter(
            class_id__in=classes.values_list("id", flat=True),
            discipline_id__in=disciplines.values_list("id", flat=True),
        )

        week_schedules = []
        today_date = (
            datetime.strptime(request.query_params["date"], "%d/%m/%Y").date()
            if "date" in request.query_params
            else date.today()
        )
        today_date += timedelta(days=1)

        for day in range(5):
            today = today_date.weekday()
            days_diff = day - today

            result = today_date + timedelta(days=days_diff)

            for current_schedule in list(schedules):

                if result.weekday() == current_schedule.weekday:
                    try:
                        wasCanceled = ClassCanceled.objects.get(
                            schedule_id=current_schedule.id,
                            canceled_date=result,
                        )
                        wasReplaced = TemporaryClass.objects.get(
                            class_canceled_id=wasCanceled.id
                        )

                        if wasReplaced.discipline_id.code not in student_disciplines:
                            current_schedule["show_replaced_class"] = False
                            continue
                    except:
                        pass

                    copy_of_schedule = copy.copy(current_schedule)
                    copy_of_schedule.date = result
                    week_schedules.append(copy_of_schedule)

        serializer = ScheduleSerializer(
            week_schedules,
            many=True,
            context={"request": request, "student_id": student_id},
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=False,
        url_path="(?P<student_id>[^/.]+)/schedules/month",
    )
    def get_month_schedules(self, request, student_id):
        student = Student.objects.get(id=student_id)

        disciplines = Discipline.objects.filter(
            id__in=student.disciplines.values_list("id", flat=True)
        )
        classes = Class.objects.filter(
            course_id=student.class_id.course_id, shift=student.class_id.shift
        )
        schedules = Schedule.objects.filter(
            class_id__in=classes.values_list("id", flat=True),
            discipline_id__in=disciplines.values_list("id", flat=True),
        )

        current_month = (
            date.today().month
            if not self.request.GET.get("month")
            else self.request.GET.get("month")
        )
        days_of_month = get_days_from_month(int(current_month))

        month_schedules = []
        queryset = list(schedules)

        month_schedules = []

        for week_schedule in days_of_month:

            for current_schedule in queryset:
                if week_schedule.weekday() == current_schedule.weekday:
                    copy_of_schedule = copy.copy(current_schedule)
                    copy_of_schedule.date = week_schedule
                    month_schedules.append(copy_of_schedule)

        serializer = ScheduleSerializer(
            month_schedules,
            many=True,
            context={"request": request, "student_id": student_id},
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=False,
        url_path="(?P<student_id>[^/.]+)/disciplines",
    )
    def get_disciplines(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            disciplines = Discipline.objects.filter(
                id__in=student.disciplines.values_list("id", flat=True)
            )
            data = []
            for i in disciplines.values():
                i["class_id"] = student.class_id
                data.append(i)
            serializer = DisciplineWithTeachSerializer(
                data, many=True, context={"request": request}
            )

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"details": "Não encontrado"}, status=status.HTTP_404_NOT_FOUND
            )


class StudentAlertViewSet(ModelViewSet):
    queryset = StudentAlert.objects.all()
    serializer_class = StudentAlertSerializer

    def create(self, request, *args, **kwargs):
        discipline = Discipline.objects.get(id=request.data["discipline_id"])
        teacher = User.objects.get(id=request.data["teacher_id"])  # Validar vínculo
        student = Student.objects.get(id=request.data["student_id"])
        reason = request.data["reason"] if "reason" in request.data else None

        alert_create = StudentAlert.objects.create(
            discipline_id=discipline,
            student_id=student,
            teacher_id=teacher,
            reason=reason,
        )
        alert_create.save()

        alert = StudentAlert.objects.last()

        serializer = StudentAlertSerializer(alert)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
