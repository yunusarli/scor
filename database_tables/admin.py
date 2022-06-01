from django.contrib import admin
from .models import Ekipman,Ekipman_Hareketi,Parca_Kodu_Listesi,Saha_Listesi,Rapor,SorguList,RaporReferanslari,SayimRapor,KontrolRaporu


class EkipmanModelAdmin(admin.ModelAdmin):
    list_display = ("parca_kodu",'saha_tipi', 'saha_no', 'saha_kodu',"seri_no","department","quantity")
    list_filter = ("saha_tipi","saha_no","saha_kodu","department")

admin.site.register(Rapor)
admin.site.register(Ekipman,EkipmanModelAdmin)
admin.site.register(Ekipman_Hareketi)
admin.site.register(Parca_Kodu_Listesi)
admin.site.register(Saha_Listesi)
admin.site.register(SorguList)
admin.site.register(RaporReferanslari)
admin.site.register(SayimRapor)
admin.site.register(KontrolRaporu)