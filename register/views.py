from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, resolve_url 
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from .forms import (
    LoginForm, UserCreateForm, UserUpdateForm, MyPasswordChangeForm,
    MyPasswordResetForm, MySetPasswordForm, EmailChangeForm
)



User = get_user_model()


class Top(generic.TemplateView):
    template_name = 'register/top.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'OMEGA FACTORING S.A.'
        return context


class Login(LoginView):
    """Página de inicio de sesión"""
    form_class = LoginForm
    template_name = 'register/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """Página de cierre de sesión"""
    template_name = 'register/top.html'


class UserCreate(generic.CreateView):
    """Registro temporal de usuarios"""
    template_name = 'register/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """Registro provisional y emisión de correo 
           electrónico para el registro completo."""
        #Cambiar entre el registro temporal y el registro principal es fácil con el atributo is_active.
        # El proceso de retiro también progresará si solo configura is_active en False.
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # Enviar URL de activación
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('register/mail_template/create/subject.txt', context)
        message = render_to_string('register/mail_template/create/message.txt', context)

        user.email_user(subject, message)
        return redirect('register:user_create_done')


class UserCreateDone(generic.TemplateView):
    """Me registré temporalmente como usuario"""
    template_name = 'register/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """Registro de usuario después de acceder a la URL en el correo electrónico"""
    template_name = 'register/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # Dentro de 1 día por defecto

    def get(self, request, **kwargs):
        """token Si es correcto, complete el registro."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # Caducado
        except SignatureExpired:
            return HttpResponseBadRequest()

        # token Esta mal
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenNo hay problema
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # Si todavía es un registro temporal y no hay otros problemas, se registrará
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class OnlyYouMixin(UserPassesTestMixin):
    """Permitir que solo el usuario o superusuario acceda a la página del usuario"""
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserDetail(OnlyYouMixin, generic.DetailView):
    """Página de detalles del usuario"""
    model = User
    template_name = 'register/user_detail.html'  # Correctamente en caso de que quiera usar el usuario predeterminadotemplate Nombreく


class UserUpdate(OnlyYouMixin, generic.UpdateView):
    """Página de actualización de información del usuario"""
    model = User
    form_class = UserUpdateForm
    template_name = 'register/user_form.html'  # Escriba el nombre de la plantilla correctamente en caso de que quiera usar el usuario predeterminadoく

    def get_success_url(self):
        return resolve_url('register:user_detail', pk=self.kwargs['pk'])


class PasswordChange(PasswordChangeView):
    """Vista de cambio de contraseñaー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('register:password_change_done')
    template_name = 'register/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """Contraseña cambiada"""
    template_name = 'register/password_change_done.html'


class PasswordReset(PasswordResetView):
    """Página de envío de URL de cambio de contraseña"""
    subject_template_name = 'register/mail_template/password_reset/subject.txt'
    email_template_name = 'register/mail_template/password_reset/message.txt'
    template_name = 'register/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('register:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """Página que envió la URL para el cambio de contraseña"""
    template_name = 'register/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """Nueva página de ingreso de contraseña"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('register:password_reset_complete')
    template_name = 'register/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """Nueva página de configuración de contraseña"""
    template_name = 'register/password_reset_complete.html'


class EmailChange(LoginRequiredMixin, generic.FormView):
    """Cambiar dirección de correo electrónico"""
    template_name = 'register/email_change_form.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        # URL Enviando
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(new_email),
            'user': user,
        }

        subject = render_to_string('register/mail_template/email_change/subject.txt', context)
        message = render_to_string('register/mail_template/email_change/message.txt', context)
        send_mail(subject, message, None, [new_email])

        return redirect('register:email_change_done')


class EmailChangeDone(LoginRequiredMixin, generic.TemplateView):
    """Envié un correo electrónico para cambiar mi dirección de correo electrónico"""
    template_name = 'register/email_change_done.html'


class EmailChangeComplete(LoginRequiredMixin, generic.TemplateView):
    """Vista de cambio de Mead llamada después de pisar un enlace"""
    template_name = 'register/email_change_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # Dentro de 1 día por defecto

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        # Caducado
        except SignatureExpired:
            return HttpResponseBadRequest()

        # token Esta mal
        except BadSignature:
            return HttpResponseBadRequest()

        # token No hay problema
        else:
            User.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)
