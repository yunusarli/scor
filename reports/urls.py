from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("bakim-raporu/",views.bakim_raporu,name="bakim_raporu"),
    path("bakim-raporu/add/",views.add_view,name="add"),
    path("bakim-raporu/save/",views.bakim_raporu_update,name="update"),
    path("bakim-raporu/delete/<int:report_id>/<str:parca_kodu>/",views.delete_view,name="delete"),
    path("bakim-raporu/send-mail/",views.send_django_mail,name="send_mail"),
    path("bakim-raporu/export/<int:rid>/",views.export_bakim_raporu,name="export"),
    path("kontrol-raporu/",views.kontrol_raporu,name="kontrol_raporu"),
    path("eht/",views.eht,name="eht"),
    path("eht/scor-calistir/",views.scor_calistir,name="scor_calistir"),
    path("envanter-listesi/",views.envanter_listesi,name="envanter_listesi"),
    path("global-rapor/",views.global_rapor,name="global_rapor"),
]