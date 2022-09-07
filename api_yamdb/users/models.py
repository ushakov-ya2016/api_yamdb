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