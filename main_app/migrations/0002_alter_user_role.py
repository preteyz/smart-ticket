# Generated by Django 4.0.3 on 2022-04-27 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Foreman', 'Foreman'), ('Project Engineer', 'Project Engineer'), ('Accounting', 'Accounting')], max_length=20),
        ),
    ]