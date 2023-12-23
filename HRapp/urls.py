from django.urls import path 
from . import views, forms
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static

from .forms import MyPasswordResetForm , MySetPasswordForm


urlpatterns = [
    path("", forms.loginForm, name ="login"),
    path("otp/", forms.otpForm, name = "otp"),
    path("home/", views.home, name ="home"),
    path("logout/", forms.logoutForm, name ="logout"),

    #password reset
    path("passwordreset/",auth_view.PasswordResetView.as_view(template_name='partials/pwdreset.html',form_class=MyPasswordResetForm), name='passwordreset'),
    path("passwordreset/done/",auth_view.PasswordResetDoneView.as_view(template_name='partials/pwdresetdone.html'), name='password_reset_done'),
    path("passwordresetconfirm/<uidb64>/<token>/",auth_view.PasswordResetConfirmView.as_view(template_name='partials/pwdresetConfirm.html',form_class=MySetPasswordForm), name='password_reset_confirm'),
    path("passwordresetcomplete/",auth_view.PasswordResetCompleteView.as_view(template_name='partials/pwdresetcomplete.html'), name='password_reset_complete'),


]
