# Generated by Django 4.0.3 on 2022-05-02 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='received_qty',
            field=models.IntegerField(),
        ),
    ]
