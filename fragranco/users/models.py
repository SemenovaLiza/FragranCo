from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=64,
        unique=True,
        verbose_name='Email'
    )
    password = models.CharField(
        max_length=200,
        verbose_name='Password'
    )
    username = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Username'
    )
    first_name = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name='First name'
    )
    last_name = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name='Last name'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'password'],
                name='unique_password_email'
            ),
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_username_email'
            ),

        ]
