# Generated by Django 4.0.7 on 2022-10-20 18:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='Электронная почта'),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('birthday', models.DateField(default='2001-01-01', verbose_name='Дата рождения')),
                ('about', models.TextField(blank=True, null=True, verbose_name='О себе')),
                ('gender', models.CharField(blank=True, choices=[('М', 'М'), ('Ж', 'Ж'), ('-', '-')], max_length=5, verbose_name='Пол')),
                ('phone_number', models.CharField(max_length=16, verbose_name='Номер телефона')),
                ('userid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]