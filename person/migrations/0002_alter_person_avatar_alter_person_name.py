# Generated by Django 4.2.1 on 2024-06-08 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='avatar',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.TextField(max_length=200),
        ),
    ]
