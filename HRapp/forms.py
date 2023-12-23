from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from . utils import send_otp
import datetime, pyotp

def loginForm(request):
    page = 'login'
     #when the user is already logged in they cant access login page via the url
    if request.user.is_authenticated:
        return redirect('home')
     

    if request.method == 'POST':
         username = request.POST.get('username')
         password = request.POST.get('password')

        #try and check if the user exists in the database
         try:
             user = User.objects.get(username=username)
         except:
             messages.error(request, 'User Does Not Exist')

        #while the user is found to exist, authenticate the user, make sure password and username match   
         user = authenticate(request, username=username, password=password)

        #while the fields are not empty and user is found then create a session for the user and redirect them to their homepage
         if user is not None:
             send_otp(request)
             request.session['username'] = username
             return redirect('otp')
         else:
             messages.error(request, 'UserName Or Password Does Not Exist!')
    return render(request, 'login.html', locals()) 

def otpForm(request):

    if request.method == 'POST':
        otp = request.POST['otp']
        username = request.session['username']

        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_date is not None:
            valid_date = datetime.datetime.fromisoformat(otp_valid_date)

            if valid_date > datetime.datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                
                if totp.verify(otp):
                    user = get_object_or_404(User, username=username)
                    login(request ,user)

                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']

                    return redirect('home')
                else:
                    messages.error(request,'Invalid OTP!')
            else:
             messages.error(request,'Your OTP has expired!')
        else:
            messages.error(request,'Something went wrong!')

    return render(request, 'partials/otp.html', locals())


def logoutForm(request):
    logout(request)
    return redirect('login')

class MyPasswordResetForm(PasswordResetForm):
    email= forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1=forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    new_password2=forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

