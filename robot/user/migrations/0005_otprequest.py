# Generated by Django 5.1.7 on 2025-03-31 20:10

import django_jalali.db.models
import phonenumber_field.modelfields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_cuser_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTPRequest',
            fields=[
                ('request_id', models.UUIDField(default=uuid.UUID('5264f7cd-7eeb-4232-9d17-e551700c6f04'), editable=False, primary_key=True, serialize=False)),
                ('reciver', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('password', models.CharField(max_length=4)),
                ('created', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
            ],
        ),
    ]
