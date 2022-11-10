from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class UserProfile(models.Model):
    MALE = 'М'
    FEMALE = 'Ж'
    HIDDEN = '-'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
        (HIDDEN, '-')
    )

    userid = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    birthday = models.DateField(verbose_name='Дата рождения', null=False, default='2001-01-01')
    about = models.TextField(verbose_name='О себе', blank=True, null=True)
    gender = models.CharField(verbose_name='Пол', choices=GENDER_CHOICES, blank=True, max_length=5)
    phone_number = models.CharField(max_length=16, verbose_name='Номер телефона')

    def __str__(self):
        return f'{self.userid.username}, ' \
               f'email: {self.userid.email}, ' \
               f'создан: {self.creation_datetime}'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(userid=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

    class Meta:
        db_table = 'auth_profile'
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
