# Generated by Django 4.2.1 on 2023-06-11 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_student_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentalert',
            name='reason',
            field=models.TextField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
