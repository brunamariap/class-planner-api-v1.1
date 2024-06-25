from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class PersonManager(BaseUserManager):
    def create_user(self, registration, password, **extra_fields):
        if not registration:
            raise ValueError('O campo registration é obrigatório')
        if not password:
            raise ValueError('O campo password é obrigatório')
        user = self.model(registration=registration, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_students(self,):
        return self.filter(department='Aluno').order_by('name')

    def get_teachers(self,):
        return self.filter(department='Professor').order_by('name')

    def get_administrator(self,):
        return self.filter(department='COADES/PF').order_by('name')


class Person(AbstractUser):
    registration = models.CharField(max_length=14, unique=True)
    name = models.TextField(max_length=200)
    avatar = models.TextField(null=True)
    department = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('staff status', default=False)
    password = models.CharField(max_length=128)

    objects = PersonManager()

    USERNAME_FIELD = 'registration'
    REQUIRED_FIELDS = ['password', ]

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        related_name='person_groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        related_name='person_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
    )
