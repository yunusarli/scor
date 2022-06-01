import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from database_tables.models import Ekipman, Ekipman_Hareketi, KontrolRaporu,Rapor, Saha_Listesi,SayimEnvanter, SayimRapor,SorguList,RaporReferanslari
import pandas as pd
from django.contrib.auth.decorators import login_required
from reports.export import ExportExcel
from scor.scor import rapor_calistir
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
from django.core.mail import BadHeaderError,EmailMessage
from .admin import SayimEnvanterResources
from django.utils.datastructures import MultiValueDictKeyError
from file_uploads.import_export import ImportFile

@login_required(login_url="users:login")
def export_bakim_raporu(request,rid):
    try:
        rapor = Rapor.objects.get(id=rid)
    except Rapor.DoesNotExist:
        return JsonResponse({
            "message":"Rapor bulunamadı"
        })
    queryset = SayimEnvanter.objects.filter(rapor=rapor)
    dataset = SayimEnvanterResources().export(queryset)
    response = HttpResponse(dataset.xlsx,content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename=bakim_raporu{rid}.xlsx'
    return response
    
@login_required(login_url="users:login")
def bakim_raporu(request):
    if request.method == "POST":
        if "rapor_id" in request.POST:
            rapor_id = request.POST.get("rapor_id",False)
            if not rapor_id:
                return render(request,"reports/bakimRaporu.html",{
                    "message": " Rapor ID boş olamaz "
                })
            try:
                rapor = Rapor.objects.get(id=rapor_id)
            except Rapor.DoesNotExist:
                return render(request,"reports/bakimRaporu.html",{
                    "message":"Rapor Bulunamadı!"
                })
            scor_listesi = SayimRapor.objects.filter(rapor=rapor)
            return render(request,"reports/bakimRaporu.html",{
                "envanterler":SayimEnvanter.objects.filter(rapor=rapor),
                "rapor_id":rapor_id,
                "scor_listesi":scor_listesi
            })
        elif "saha_no" in request.POST:
            #scora kaydetme işlemlerinin de yapılması gerekiyor
            saha_no = request.POST.get("saha_no",False)
            if not saha_no:
                return render(request,"reports/bakimRaporu.html",{
                    "message":" Saha numarası boş girilemez "
                })
            #ekipmanlar = Ekipman.objects.filter(saha_no=saha_no)
            ekipmanlar = Ekipman.objects.filter(Q(saha_no=saha_no) | Q(saha_kodu=saha_no))
            if len(ekipmanlar) == 0:
                return render(request,"reports/bakimRaporu.html",{
                    "message": " Bu saha numarasına air ekipman bulunmamaktadır "
                })
            
            rapor = Rapor.objects.create(
                saha_no=saha_no,
                create_user=request.user
            )
            rapor.save()
            sayim_listesi = list()
            for ekipman in ekipmanlar:
                sayim = SayimEnvanter.objects.create(
                    rapor=rapor,
                    **ekipman.serialize()
                )
                sayim.save()
                sayim_listesi.append(sayim)
            sorgu_list = pd.DataFrame(SorguList.objects.all().values("sorgu_no", "kontrol", "ref_grup", "kategori", "check_analyze"))
            sorgu_ref = pd.DataFrame(RaporReferanslari.objects.all().values("sorgu_no", "ref", "ekipman_parca_kodu", "parca_tanimi", "grup_tanimi", "ref_grup", "kategori"))
            ham_veri = pd.DataFrame([ekipman.serialize() for ekipman in ekipmanlar])
            rapor_calistir(ham_veri,sorgu_list,sorgu_ref,rapor)
            scor_listesi = SayimRapor.objects.filter(rapor=rapor)
            return render(request,"reports/bakimRaporu.html",{
                "envanterler":sayim_listesi,
                "rapor_id":rapor.id,
                "scor_listesi":scor_listesi
            })
            
        return render(request,"reports/bakimRaporu.html")
    else:
        return render(request,"reports/bakimRaporu.html")

@login_required(login_url="users:login")
def kontrol_raporu(request):
    if request.method == "POST":

        rapor_id = request.POST.get("kontrol_id",False)
        
        try:
            rapor = Rapor.objects.get(id=rapor_id)
        except Rapor.DoesNotExist:
            return render(request,"reports/kontrolRaporu.html",{"message":"Rapor bulunamadı"})
        kontroller = KontrolRaporu.objects.filter(rapor)
        if len(kontroller) > 0:
            return render(request,"reports/kontrolRaporu.html",{"message":"Daha önce bu raporla bir kontrol yapılmıştır. Sonuçlarını aşağıdan görebilirsiniz."})
        sayim_envanter = SayimEnvanter.objects.filter(rapor=rapor)

        file = request.FILES["secret_kontrol_file"]
        excel = pd.read_excel(file)
        excel_to_dict = excel.to_dict(orient="records")

        for obj in excel_to_dict:
            seri_no = obj["Seri No"]
            if seri_no:
                for envanter in sayim_envanter:
                    if envanter.seri_no == seri_no:
                        if envanter.sayim == obj["Miktar"]:
                            sonuc = "Uyumlu"
                        else:
                            sonuc = "Uyumsuz"
                        sayim_fark = envanter.sayim - obj["Miktar"]
                        lokasyon = envanter.saha_kodu
                        aciklama = envanter.aciklama
            else:
                parca_kodu = obj["Parça Kodu"]
                for envanter in sayim_envanter:
                    if envanter.parca_kodu == parca_kodu:
                        if envanter.sayim == obj["Miktar"]:
                            sonuc = "Uyumlu"
                        else:
                            sonuc = "Uyumsuz"
                        sayim_fark = envanter.sayim - obj["Miktar"]
                        lokasyon = envanter.saha_kodu
                        aciklama = envanter.aciklama
            parca_kodu = obj["Parça Kodu"]
            parca_tanimi = obj["Parça Tanımı"]
            miktar = obj["Miktar"]

            kontrol = KontrolRaporu.objects.create(
                rapor=rapor,
                parca_kodu=parca_kodu,
                parca_tanimi = parca_tanimi,
                miktar=miktar,
                sayim_fark = sayim_fark,
                sonuc = sonuc,
                lokasyon = lokasyon,
                aciklama = aciklama
                )
            kontrol.save()

        kontroller = KontrolRaporu.objects.filter(rapor=rapor)
        return render(request,"reports/kontrolRaporu.html",{"kontroller":kontroller})
            
            
            
           

    return render(request,"reports/kontrolRaporu.html")

@login_required(login_url="users:login")
@csrf_exempt
def scor_calistir(request):
    """ EHT için scorun çalıştırılması """
    data = json.loads(request.body)
    saha_no = data.get("saha_no")
    parca_kodlari = data.get("parca_kodlari")
    scora_gidecekler = []
    print(parca_kodlari)
    ekipmanlar = Ekipman_Hareketi.objects.filter(hedef_lokasyon=saha_no)
    for ekipman in ekipmanlar:
        if ekipman.parca_kodu in parca_kodlari:
            scora_gidecekler.append(ekipman)
    try:
        saha = Saha_Listesi.objects.get(Q(saha_no=saha_no) | Q(saha_kodu=saha_no))
    except:
        return JsonResponse({"message":"Belirtilen saha numarasına ait saha numarası bulunamadı ya da birden fazla mevcut."})
    saha_no = saha.saha_no
    rapor = Rapor.objects.create(create_user=request.user,saha_no=saha.saha_no)
    rapor.save()
    #saha_no, saha_kodu,parca_kodu,departman,quantity
    obj_list = []
    for _ in scora_gidecekler:
        obj = {}
        obj["saha_no"] = saha_no
        obj["quantity"] = int(_.islem_miktari)
        obj["ekipman_parca_kodu"] = _.parca_kodu
        obj["saha_kodu"] = saha.saha_kodu
        obj["department"] = saha.department
        obj_list.append(obj)

    sorgu_list = pd.DataFrame(SorguList.objects.all().values("sorgu_no", "kontrol", "ref_grup", "kategori", "check_analyze"))
    sorgu_ref = pd.DataFrame(RaporReferanslari.objects.all().values("sorgu_no", "ref", "ekipman_parca_kodu", "parca_tanimi", "grup_tanimi", "ref_grup", "kategori"))
    ham_veri = pd.DataFrame(obj_list)
    rapor_calistir(ham_veri,sorgu_list,sorgu_ref,rapor)
    sonuclar = SayimRapor.objects.filter(rapor=rapor)
    return JsonResponse([sonuc.serialize() for sonuc in sonuclar],safe=False)

@login_required(login_url="users:login")
def eht(request):
    if request.method == "POST":
        saha_no = request.POST.get("saha_no")
        ehts = Ekipman_Hareketi.objects.filter(hedef_lokasyon=saha_no)
        return render(request,"reports/eht.html",{"ehts":ehts,"saha_no":saha_no})

    return render(request,"reports/eht.html")

@login_required(login_url="users:login")
def envanter_listesi(request):
    if request.method == "POST":
        saha_no = request.POST.get("saha_no")
        envanterler = Ekipman.objects.filter(Q(saha_no=saha_no) | Q(saha_kodu=saha_no))
        return render(request,"reports/envanter_listesi.html",{
            "envanterler":envanterler
        })
    return render(request,"reports/envanter_listesi.html") 

@login_required(login_url="users:login")
def global_rapor(request):
    return render(request,"reports/globalRapor.html")

@login_required(login_url="users:login")
@csrf_exempt
def add_view(request):
    data = json.loads(request.body)
    id = data.get("report_id")

    print(data)
    
    try:
        rapor = Rapor.objects.get(id=int(id))
    except Rapor.DoesNotExist:
        return JsonResponse({"message":"Rapor Bulunamadı"})
    
    print("DATA:   ",data)
    
    sayim = SayimEnvanter.objects.create(
        rapor=rapor,
        parca_kodu=data.get("parca_kodu"),
        parca_tanimi=data.get("parca_tanimi"),
        quantity=int(data.get("quantity")),
        sayim=data.get("sayim"),
        aciklama=data.get("aciklama")
        )
    sayim.save()
    return JsonResponse(sayim.serialize())

@login_required(login_url="users:login")
@csrf_exempt
def bakim_raporu_update(request):
    if request.method == "POST":
        data = json.loads(request.body)
        for object in data.get("objects"):
            try:
                sayim = SayimEnvanter.objects.get(id=int(object["id"]))
            except SayimEnvanter.DoesNotExist:
                pass
            sayim.sayim = int(object["sayim"])
            sayim.aciklama = object["description"] 
            sayim.save()
        return JsonResponse({"message":"Güncellemeler başarılı! Not: Eğer şu an sayfada bulunmayan bir elemanı güncellediyseniz, güncelleme veri tabanına etki etmez. Aşağıdan all seçeneğini tıklayıp tekrar denemeniz gerekir!"})


    else:
        return JsonResponse({'message':'Bu metoda izin verilmiyor'})
    
@login_required(login_url="users:login")
@csrf_exempt
def delete_view(request,report_id,parca_kodu):
    try:
        sayim = SayimEnvanter.objects.get(Q(report=Rapor.objects.get(id=report_id)) & Q(parca_kodu=parca_kodu) )
    except (SayimEnvanter.DoesNotExist, Rapor.DoesNotExist):
        return JsonResponse({"message":"Rapor ve Envanter Bulunamadı"})
    
    return JsonResponse({"message":"Envanter başarı ile silindi"})

@login_required(login_url="users:login")
@csrf_exempt    
def send_django_mail(request):
    data = json.loads(request.body)
    rapor_id = data.get('report_id',False)
    if rapor_id:
        rapor = Rapor.objects.get(id=rapor_id)
        envanterler = SayimRapor.objects.filter(rapor=rapor)
        subject = "Rapor bilgilendirmesi"
        message = "{} id'li rapora ait scor tablosu".format(rapor.id)
        recipients = ["yunusarlivdl@gmail.com"]
    else:
        return JsonResponse({'message':'Rapor id bilgisi ulaşmadı'})
    try:
        email = EmailMessage(subject=subject, body=message, from_email="rapor@scor-app.com",
                         to=recipients)
        path = ExportExcel().generate_scor_excel(envanterler)
        if os.path.exists(path):
            with open(path,"rb") as excel:
                data = excel.read()
        email.attach("demo.xlsx",data,'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        email.send()
                         
    except BadHeaderError:
        return JsonResponse({'message':"Bad header selected"})
    return JsonResponse({'message':'Mail başarı ile gönderildi.Eğer mail iletimi görmüyosanız, spam kutunuzu kontrol ediniz.'})
