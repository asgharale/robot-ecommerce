# Generated by Django 5.1.7 on 2025-03-24 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cuser',
            options={'ordering': ('id',)},
        ),
        migrations.AddField(
            model_name='cuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='cuser',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
