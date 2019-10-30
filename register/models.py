from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from apps.validators import validaRut

class UserManager(BaseUserManager):
    """Administrador de usuariosー"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a user with the given username, email, and
        password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuario personalizado

    username Sin usar、email La dirección se usa como nombre de usuario.

    """
    email = models.EmailField(_('dirección de correo electrónico'), unique=True)
    first_name = models.CharField(_('Nombre'), max_length=30, blank=True)
    last_name = models.CharField(_('Apellido'), max_length=150, blank=True)
    rut = models.CharField(_('Rut'), validators= [validaRut], max_length=10,blank=True, help_text="Ejemplo: 1111111-1")

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designa si el usuario puede iniciar sesión en este sitio de administración.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designa si este usuario debe ser tratado como activo. '
            'Anule la selección de esto en lugar de eliminar cuentas.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """Devuelve el primer nombre más el último nombre, con un espacio"""
        full_name = '%s %s' % (self.first_name, self.last_name, self.rut)
        return full_name.strip()

    def get_short_name(self):
        """Devuelve el nombre corto para el usuario."""
        return self.first_name

    def get_rut_name(self):
        """Devuelve el rut."""
        return self.rut

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Enviar un correo electrónico a este usuario."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        return self.email
