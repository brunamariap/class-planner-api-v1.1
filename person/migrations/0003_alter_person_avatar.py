# Generated by Django 4.2.1 on 2024-06-20 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_alter_person_avatar_alter_person_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='avatar',
            field=models.TextField(null=True),
        ),
    ]