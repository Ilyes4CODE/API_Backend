# Generated by Django 5.0.2 on 2024-03-19 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0009_client_email_client_first_name_client_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='average_time_person',
            field=models.IntegerField(null=True),
        ),
    ]
