from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField
from account.managers import UserManager


class User(AbstractUser):
    CLIENT = 'client'
    SALESMAN = 'salesman'
    ADMIN = 'admin'

    ROLE = (
        (CLIENT, 'Покупатель'),
        (SALESMAN, 'Продавец'),
        (ADMIN, 'Администратор')
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('-date_joined',)

    username = None
    avatar = models.ImageField(upload_to='avatars/', verbose_name='аватарка', null=True, blank=True)
    phone = PhoneNumberField(max_length=100, verbose_name='номер телефона')
    email = models.EmailField(blank=True, verbose_name='электронная почта', unique=True)
    role = models.CharField('роль', choices=ROLE, default=CLIENT, max_length=15)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    get_full_name.fget.short_description = 'полное имя'

    def __str__(self):
        return f'{self.email or str(self.phone)}'


# Create your models here.