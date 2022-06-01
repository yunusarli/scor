from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from database_tables.models import Parca_Kodu_Listesi, Saha_Listesi

@login_required(login_url="users:login")
def saha_listesi(request):
    saha_listesi = Saha_Listesi.objects.all()
    return render(request,"database_tables/saha_listesi.html",{"saha_listesi":saha_listesi})

@login_required(login_url="users:login")
def parca_kodlari(request):
    parca_kodlari = Parca_Kodu_Listesi.objects.all()
    return render(request,"database_tables/parca_kodu.html",{"parca_kodu_listesi":parca_kodlari})