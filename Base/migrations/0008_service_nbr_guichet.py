# Generated by Django 5.0.2 on 2024-03-09 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0007_service_qte'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='nbr_guichet',
            field=models.IntegerField(null=True),
        ),
    ]
