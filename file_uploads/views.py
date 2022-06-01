from re import S
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from .import_export import ImportFile
from database_tables.models import Ekipman, Ekipman_Hareketi, Parca_Kodu_Listesi, RaporReferanslari, Saha_Listesi, SorguList
from .tasks import celery_upload_file_task
from django.contrib.auth.decorators import login_required

@login_required(login_url="users:login")
def upload_file_view(request):
    return render(request,"file_uploads/import.html")

@login_required(login_url="users:login")
@csrf_exempt
def upload_file_to_database(request):
    """ Veri tabanında dosyaların yüklenmesi.
        Ekipmanlar veya eht dosyalaarının veri tabanına yüklenmesi
    """
    if request.method == "POST":
        #gelen dosyayı alma
        file = request.FILES.get("file")
        #dosyanın tipini alma
        db_type = request.POST.get("type")

        if db_type.lower() == "envanter":
            db = Ekipman
            instance = ImportFile(file,db).import_envanter()
        # elif db_type.lower() == "sorgu_list":
        #     db = SorguList
        # elif db_type.lower() == "rapor_referanslari":
        #     db = RaporReferanslari
        else:
            db = Ekipman_Hareketi
            instance = ImportFile(file,db).import_eht()
        if instance == "Error":
            return JsonResponse({"message":"Bir Hata Oluştu"})
        return JsonResponse({"message":"Veriler başarılı bir şekilde yüklendi!"})
    else:
        return JsonResponse({'message':"Method is not allowed!"})

@login_required(login_url="users:login")
@csrf_exempt
def update_parca_kodu(request):
    """ Parça kodlarının güncellenmesi """
    #eski kayıtların silinmesi (aksi takdirde hepsinin teker teker varlığı sorgulanmak zorunda kalınırdı)
    Parca_Kodu_Listesi.objects.all().delete()
    #unique olarak yeni parçaların veri tabanından çekilmesi
    yeni_parca = Ekipman.objects.all().values_list("parca_kodu","parca_tanimi").distinct()
    values = [{"parca_kodu":parca_kodu,"parca_tanimi":parca_tanimi} for parca_kodu,parca_tanimi in yeni_parca]
    parca_list = list()

    for parca in values:
        prc = Parca_Kodu_Listesi(**parca)
        parca_list.append(prc)
    Parca_Kodu_Listesi.objects.bulk_create(parca_list,batch_size=9999)

    for parca in Parca_Kodu_Listesi.objects.all():
        try:
            eht = Ekipman_Hareketi.objects.filter(parca_kodu=parca.parca_kodu)[0]
        except IndexError:
            continue
        parca.parca_tipi = eht.ekipman_tipi
        parca.birim = eht.olcum_birimi
        parca.save()

    return JsonResponse({"message":"Parçalarınız başarılı bir şekilde güncellenmiştir."})

@login_required(login_url="users:login")
@csrf_exempt
def update_saha_listesi(request):
    """ Saha Listesinin güncellenmesi """
    #tün saha listelerinin silinmesi
    Saha_Listesi.objects.all().delete()

    yeni_saha = Ekipman.objects.all().values_list("saha_kodu","saha_tipi","saha_no","department").distinct()
    values = [{"saha_kodu":saha_kodu,"saha_tipi":saha_tipi,"saha_no":saha_no,"department":department} for saha_kodu,saha_tipi,saha_no,department in yeni_saha]
    saha_list = list()
    for saha in values:
        print(saha)
        sh = Saha_Listesi(**saha)
        saha_list.append(sh)
    Saha_Listesi.objects.bulk_create(saha_list,batch_size=9999)

    return JsonResponse({"message":"Saha Listesi Başarılı bir şekilde güncellenmiştir."})

@login_required(login_url="users:login")
@csrf_exempt
def update_global_rapor(request):
    """ Global raporun güncellenmesi """
    pass
