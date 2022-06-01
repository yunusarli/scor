from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.db import IntegrityError
from users.models import UserProfile
from .forms import CaptchaTestForm

def home(request):
    return render(request,"users/welcome.html")

def login_view(request):

    captcha_form = CaptchaTestForm() 
    if request.method == "POST": 
        validated_form = CaptchaTestForm()
        message = ""
        email = request.POST.get("email")
        password = request.POST.get("password")

        if email and password:
            user = authenticate(email=email,password=password)
            if not (user is None):
                login(request,user)
                return HttpResponseRedirect(reverse("users:home"))
            else:
                message = "Kullanıcı Bulunamadı"
        else:
            message = "Lütfen Kullanıcı adı ve şifrenizi giriniz."

        return render(request,"users/login.html",{"message":message,"form":captcha_form})
    else:
        
        return render(request,"users/login.html",{"form":captcha_form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("users:login"))

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        if not (password and password==confirmation):
            return render(request,"users/register.html",{"message":"Şifreler eşleşmiyor"})
        
        try:
            user = UserProfile.objects.create_user(
                username=username,
                password=password
            )
            user.save()
        except IntegrityError:
            return render(request,"users/register.html",{"message":"Bu isimde bir kullanıcı zaten var"})
        login(request,user)
        return HttpResponseRedirect(reverse("users:home"))
    else:
        return render(request,"users/register.html")