import jwt, uuid
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Создает и возвращает пользователя с имэйлом, паролем и именем.
        """
        if username is None:
            raise TypeError('Users must have a username.')

        # user = self.model(username=username, email=self.normalize_email(email))
        user = self.model(username=username)
        if password:
            user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password):
        """
        Создает и возвращет пользователя с привилегиями суперадмина.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        # return token.decode('utf-8')
        return token


class Profile(models.Model):
    user_id = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_profile',
        verbose_name=_('Пользователь')
    )
    first_name = models.CharField(
        max_length=150, verbose_name=_('Имя')
    )
    last_name = models.CharField(
        max_length=150, verbose_name=_('Фамилия')
    )
    avatar = models.ImageField(upload_to='users/', blank=True, null=True)
    birth_date = models.DateField(verbose_name=_('Дата рождения'))
    phone_number = PhoneNumberField(blank=True, null=True, unique=True, verbose_name=_('Номер телефона'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Профиль')
        verbose_name_plural = _('Профили')

    def __str__(self):
        return f"{self.email}"

