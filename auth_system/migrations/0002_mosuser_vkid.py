# Generated by Django 3.0.1 on 2020-04-13 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mosuser',
            name='vkId',
            field=models.BigIntegerField(null=True, verbose_name='VK ID'),
        ),
    ]