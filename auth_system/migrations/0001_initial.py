# Generated by Django 3.0.1 on 2020-03-23 14:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MosUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mosLogin', models.CharField(max_length=50, verbose_name='Mos.ru login')),
                ('mosPassword', models.CharField(max_length=50, verbose_name='Mos.ru password')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, default='00', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Mos.ru user',
                'verbose_name_plural': 'Mos.ru users',
            },
        ),
    ]
