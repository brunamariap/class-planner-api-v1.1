# Generated by Django 4.2.1 on 2023-07-18 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_teacher_email'),
        ('course', '0005_alter_course_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classcanceled',
            name='is_available',
        ),
        migrations.RemoveField(
            model_name='classcanceled',
            name='quantity_available',
        ),
        migrations.RemoveField(
            model_name='classcanceled',
            name='teacher_ids',
        ),
        migrations.AddField(
            model_name='classcanceled',
            name='teacher_id',
            field=models.ForeignKey(blank=True, db_column='teacher_id', default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='teacher.teacher'),
            preserve_default=False,
        ),
    ]
