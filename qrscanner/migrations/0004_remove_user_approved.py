# Generated by Django 5.0.3 on 2024-09-25 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qrscanner', '0003_user_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='approved',
        ),
    ]
