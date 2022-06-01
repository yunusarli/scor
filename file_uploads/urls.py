from django.urls import path
from . import views

app_name = "file_uploads" 

urlpatterns = [
    path("panel/",views.upload_file_view,name="upload"),
    path("panel/upload/",views.upload_file_to_database,name="to_database"),
    path("panel/update-saha-listesi/",views.update_saha_listesi,name="update_saha_listesi"),
    path("panel/update-parca-kodu/",views.update_parca_kodu,name="update_parca_kodu"),
]