from django.urls import path
from . import views

app_name = "parca_kodlari"

urlpatterns = [
    path("saha-listesi/",views.saha_listesi,name="saha_listesi"),
    path("parca-kodlari-listesi/",views.parca_kodlari,name="parca_kodlari"),
]