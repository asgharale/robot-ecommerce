# Generated by Django 5.1.7 on 2025-03-29 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_cuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuser',
            name='email',
            field=models.EmailField(blank=True, max_length=255),
        ),
    ]
