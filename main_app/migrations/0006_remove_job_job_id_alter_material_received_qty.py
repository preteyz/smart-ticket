# Generated by Django 4.0.3 on 2022-04-26 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_remove_job_invoices_remove_job_tickets_job_job_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='job_id',
        ),
        migrations.AlterField(
            model_name='material',
            name='received_qty',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]