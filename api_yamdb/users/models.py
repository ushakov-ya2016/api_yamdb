from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER_ROLES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )

    bio = models.TextField(
        max_length=300,
        blank=True,
    )

    role = models.CharField(
        max_length=20,
        choices=USER_ROLES,
        default='user',
    )

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        null=True,
        unique=True
    )

    email = models.EmailField(verbose_name='email', unique=True, blank=False)
    confirmation_code = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username, ']

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'self.user'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('username',)

    def __str__(self):
        return self.email
