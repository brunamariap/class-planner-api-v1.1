from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from course.api.viewsets import CourseViewSet, ClassViewSet, DisciplineViewSet, ScheduleViewSet, TemporaryClassViewSet, ImportDisciplineGenericView, DeleteDisciplineLinkView

from teacher.api.viewsets import TeacherViewSet, TeacherClassesViewSet, TeacherDisciplinesViewSet, TeacherBindingViewSet

from student.api.viewsets import StudentViewSet, StudentAlertViewSet
from person.api.viewsets import RegisterUserAPIView
from person.views import SuapAPIAuth

router = routers.SimpleRouter()

router.register('courses', CourseViewSet)
router.register('classes', ClassViewSet)
router.register('disciplines', DisciplineViewSet)
router.register('teachers', TeacherViewSet)
router.register('students', StudentViewSet)
router.register('alerts', StudentAlertViewSet)
router.register('schedules', ScheduleViewSet)
router.register('temporary-classes', TemporaryClassViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path(
        'api/teachers/disciplines/<int:pk>/',
        TeacherBindingViewSet.as_view()
    ),
    path(
        'api/courses/<int:course>/disciplines/import/',
        ImportDisciplineGenericView.as_view()
    ),
    path(
        'api/courses/<int:course>/disciplines/<int:discipline>/',
        DeleteDisciplineLinkView.as_view()
    ),
    path(
        'api/teachers/<int:teacher>/disciplines/',
        TeacherDisciplinesViewSet.as_view()
    ),
    path(
        'api/teachers/<int:teacher>/classes/',
        TeacherClassesViewSet.as_view()
    ),

    # Auth
    path('api/users/register/', RegisterUserAPIView.as_view(), name='register'),
    # path('api/users/login/', RegisterUserAPIView.as_view(), name='register'),

    # Swagger docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path(
        'api/docs/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),

    # Tokens
    # path(
    #     'api/token/',
    #     TokenObtainPairView.as_view(),
    #     name='token_obtain_pair'
    # ),
    path(
        'api/token/',
        SuapAPIAuth.as_view(),
        name='token_obtain_pair',
    ),
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'api/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
]
