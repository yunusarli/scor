from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Departmanlar(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name

class DepartmentEmails(models.Model):
    department = models.ForeignKey(Departmanlar,on_delete=models.CASCADE)
    email = models.CharField(max_length=300)


    def __str__(self):
        return f"{self.department} departmanına ait {self.email} maili"

class Ekipman(models.Model):
    """ Raporumuzu hazırlayacağımız ekipman veri tabanımız. (Parça kodları da buradan çağrılıyor.)"""
    saha_tipi = models.CharField(max_length=255,blank=True,null=True)
    saha_no = models.CharField(max_length=255,blank=True,null=True)
    saha_kodu = models.CharField(max_length=400,blank=True,null=True)
    parca_kodu = models.CharField(max_length=255,blank=True,null=True)
    parca_tanimi = models.CharField(max_length=600)
    seri_no = models.CharField(max_length=400,default="")
    department = models.CharField(max_length=250,blank=True,null=True)
    ana_yer_tipi = models.CharField(max_length=255,blank=True,null=True)
    quantity = models.IntegerField(default=1)
    teslim_tarihi = models.CharField(max_length=255,blank=True,null=True)
    sahaya_kurulum_tarihi = models.CharField(max_length=255,blank=True,null=True)
    ust_ekipman = models.CharField(max_length=300,blank=True,null=True)

    def __str__(self):
        return self.parca_kodu
    
    def serialize(self):
        return {
            'saha_tipi':self.saha_tipi,
            'saha_no':self.saha_no,
            'saha_kodu':self.saha_kodu,
            'parca_kodu':self.parca_kodu,
            'parca_tanimi':self.parca_tanimi,
            'seri_no':self.seri_no,
            'department':self.department,
            'ana_yer_tipi':self.ana_yer_tipi,
            'quantity':self.quantity,
            'teslim_tarihi':self.teslim_tarihi,
            'sahaya_kurulum_tarihi':self.sahaya_kurulum_tarihi,
            'ust_ekipman':self.ust_ekipman
        }


class TemporaryExcelFiles(models.Model):
    """ Excel dosyaları üzerinde işlem yapabilmek için kurduğumuz geçici bir 
    veri tabanı (her işlemden sonra temizlenir.)
     """
    file = models.FileField(upload_to='sheets/')
    

# Ekipman Parça Kodu BazlÄ± Hareket listesi
class Ekipman_Hareketi(models.Model):
    islem_no = models.CharField(max_length=500,blank=True,null=True)
    islem_tarihi = models.CharField(max_length=500,blank=True,null=True)
    parca_kodu = models.CharField(max_length=500,blank=True,null=True)
    parca_tanimi = models.CharField(max_length=500,blank=True,null=True)
    islem_miktari = models.IntegerField(blank=True,null=True)
    olcum_birimi = models.CharField(max_length=500,blank=True,null=True)
    kaynak_yeri = models.CharField(max_length=500,blank=True,null=True)
    kaynak_adresi = models.CharField(max_length=500,blank=True,null=True)
    transfer_yeri = models.CharField(max_length=500,blank=True,null=True)
    transfer_adresi = models.CharField(max_length=500,blank=True,null=True)
    islem_tipi = models.CharField(max_length=500,blank=True,null=True)
    kaynak_surec = models.CharField(max_length=500,blank=True,null=True)
    form_no = models.CharField(max_length=500,blank=True,null=True)
    kaynak_departman = models.CharField(max_length=500,blank=True,null=True)
    hedef_departman = models.CharField(max_length=500,blank=True,null=True)
    hedef_lokasyon = models.CharField(max_length=500,blank=True,null=True)
    kullanici_adi = models.CharField(max_length=500,blank=True,null=True)
    ekipman_tipi = models.CharField(max_length=500,blank=True,null=True)
    referans = models.CharField(max_length=500,blank=True,null=True)

    def __str__(self):
        return self.islem_no
    
    def serialize(self):
        return {
            'id':self.id,
            "islem_no": self.islem_no,
            "islem_tarihi": self.islem_tarihi,
            "parca_kodu": self.parca_kodu,
            "parca_tanimi": self.parca_tanimi,

            "islem_miktari": self.islem_miktari,
            "olcum_birimi": self.olcum_birimi,
            "kaynak_yeri": self.kaynak_yeri,
            "kaynak_adresi": self.kaynak_adresi,
            "transfer_yeri": self.transfer_yeri,
            "transfer_adresi": self.transfer_adresi,
            "islem_tipi":self.islem_tipi,
            "kaynak_surec": self.kaynak_surec,
            "form_no": self.form_no,
            "kaynak_departman": self.kaynak_departman,
            "hedef_departman": self.hedef_departman,
            "hedef_lokasyon": self.hedef_lokasyon,
            "kullanici_adi": self.kullanici_adi,
            "ekipman_tipi": self.ekipman_tipi,
            "referans": self.referans
        }



# Envanterde bulunan parÃ§a kodlarÄ±na ait kÃ¼tÃ¼k
class Parca_Kodu_Listesi(models.Model):
    """ Raporumuzu hazÄ±rlayacaÄŸÄ±mÄ±z ekipman veri tabanÄ±mÄ±z. """
    parca_kodu = models.CharField(max_length=255,blank=True,null=True)
    parca_tanimi = models.CharField(max_length=600)
    birim = models.CharField(max_length=40,null=True,blank=True)
    parca_tipi = models.CharField(max_length=40)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    ana_kategori = models.CharField(max_length=255,blank=True,null=True)
    alt_kategori = models.CharField(max_length=255,blank=True,null=True)
    ana_ekipman = models.CharField(max_length=300,blank=True,null=True)
    alt_ekipman = models.CharField(max_length=300,blank=True,null=True)
    
    def __str__(self):
        return self.parca_kodu
    
    def serialize(self):
        return {
            'id':self.id,
            'parca_kodu':self.parca_kodu,
            'parca_tanimi':self.parca_tanimi,
            'birim':self.birim,
            'parca_tipi':self.parca_tipi,
            'ana_kategori':self.ana_kategori,
        }

# Envanterde bulunan parÃ§a kodlarÄ±na ait resimler
class Parca_Kodu_Listesi_Resimleri(models.Model):
    resim = models.ImageField(upload_to="images/",null=True,blank=True)
    parca_kodu = models.ForeignKey(Parca_Kodu_Listesi,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.parca_kodu.parca_kodu} ekipmanına ait resim"

# Envanterde ki sahalarÄ±n listesi
class Saha_Listesi(models.Model):
    """ Raporumuzu hazÄ±rlayacaÄŸÄ±mÄ±z ekipman veri tabanÄ±mÄ±z. """
    saha_no = models.CharField(max_length=255,blank=True,null=True)
    saha_kodu = models.CharField(max_length=400,blank=True,null=True)
    department = models.CharField(max_length=250,blank=True,null=True)
    ana_yer_tipi = models.CharField(max_length=400,blank=True,null=True)
    saha_tipi = models.CharField(max_length=400,blank=True,null=True)
    STATUS_CHOISES = [
        ('A','Aktif'),
        ('P','Pasif'),
    ]
    status = models.CharField(max_length=2,choices=STATUS_CHOISES,default="A")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)


from users.models import UserProfile

class Rapor(models.Model):
    """ sayim ve soucun birliğini sağlamak için oluşturulan yapı. """
    ONAY_SECENEKLERI = [
        ('O','Onaylı'),
        ('H','Hata'),
        ('B','Bekliyor'),
        ('I','Iptal'),
    ]
    onay = models.CharField(choices=ONAY_SECENEKLERI,default='B',max_length=10)
    saha_no = models.CharField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    updated_user = models.ManyToManyField(UserProfile,related_name="updated_user",blank=True)
    create_user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    rapor_type = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return f"{self.saha_no}'ya ait {self.id} ID'li rapor"

    
class SayimEnvanter(models.Model):
    """ Teker teker ekipmanlara rapor id atanarak oluşturulan sayım kısmı """
    rapor = models.ForeignKey(Rapor,on_delete=models.CASCADE)
    saha_tipi = models.CharField(max_length=100,blank=True,null=True)
    saha_no = models.CharField(max_length=100,blank=True,null=True)
    saha_kodu = models.CharField(max_length=400,blank=True,null=True)
    parca_kodu = models.CharField(max_length=100,blank=True,null=True)
    parca_tanimi = models.CharField(max_length=600,blank=True,null=True)
    seri_no = models.CharField(max_length=400,default="")
    department = models.CharField(max_length=250,blank=True,null=True)
    ana_yer_tipi = models.CharField(max_length=255,blank=True,null=True)
    quantity = models.IntegerField(default=1)
    teslim_tarihi = models.CharField(max_length=255,blank=True,null=True)
    sahaya_kurulum_tarihi = models.CharField(max_length=255,blank=True,null=True)
    ust_ekipman = models.CharField(max_length=300,blank=True,null=True)
    sayim = models.PositiveIntegerField(default=0)
    aciklama = models.CharField(max_length=400,blank=True,null=True)
    resim = models.ImageField(upload_to="sayim_resimleri/",blank=True,null=True)
    is_came_out = models.BooleanField(default=False)#dışardan gelen elemanlrı silme işlemi için

    def __str__(self):
        return f"{self.rapor.id} ID'li rapora ait olan {self.parca_kodu} Parça kodlu ekipman."
    
    def serialize(self):
        return {
            'rapor':self.rapor.id,
            'ekipman':self.parca_kodu,
            'saha_no':self.saha_no,
            'saha_kodu':self.saha_kodu,
            'department':self.department,
            'seri_no':self.seri_no,
            'parca_tanimi':self.parca_tanimi,
            'quantity':self.quantity,
            'sayim':self.sayim,
            'aciklama':self.aciklama,
            'is_came_out':self.is_came_out,
        }


class KontrolEnvanterScor(models.Model):
    """ üzerinde çalışılacak algoritma ile konuşan tablomuz bu. """
    sayim_envanter = models.ForeignKey(SayimEnvanter,on_delete=models.CASCADE)
    referans1 = models.IntegerField()
    referans2 = models.IntegerField()
    referans3 = models.IntegerField()
    sonuc = models.CharField(max_length=400)
    kategori = models.CharField(max_length=400)
    alt_kategori = models.CharField(max_length=400)
    ana_kategori = models.CharField(max_length=400)
    sorgu_num = models.CharField(max_length=400)
    



class SayimRapor(models.Model):
    saha_no = models.CharField(verbose_name="Saha No", max_length=50, default="")
    saha_kod = models.CharField(verbose_name="Saha Kod", max_length=50, default="")
    ref_1 = models.IntegerField(verbose_name="Referans-1")
    ref_2 = models.IntegerField(verbose_name="Referans-2")
    ref_3 = models.IntegerField(verbose_name="Referans-3")
    ref_4 = models.IntegerField(verbose_name="Referans-4")
    ref_5 = models.IntegerField(verbose_name="Referans-5")
    ref_6 = models.IntegerField(verbose_name="Referans-6")
    ref_grup = models.CharField(verbose_name="Ref Grup", max_length=5000, default="")
    sonuc = models.CharField(verbose_name="Sonuç", max_length=50, default="")
    kontrol = models.CharField(verbose_name="Kontrol", max_length=5000, default="")
    kategori = models.CharField(verbose_name="Kategori", max_length=50, default="")
    sorgu_no = models.CharField(verbose_name="Sorgu No", max_length=50, default="")
    aciklama = models.CharField(verbose_name="Açıklama", max_length=5000,blank=True,null=False, default="")
    rapor = models.ForeignKey(Rapor, related_name="girdiler", on_delete=models.CASCADE)

    is_sayim_sonrasi = models.BooleanField(verbose_name="Sayım Sonrası Girdisi Mi?", default=False)
    created_at = models.DateTimeField(verbose_name="Oluşturulma Tarihi", auto_now_add=True)

    class Meta:
        verbose_name = "Kontrol Uyumsuzluk Rapor"
        verbose_name_plural = "Kontrol Uyumsuzluk Raporları"

    def __str__(self):
        return self.kontrol
    
    def serialize(self):
        return {
            'saha_no':self.saha_no,
            'saha_kod':self.saha_kod,
            'ref_1':self.ref_1,
            'ref_2':self.ref_2,
            'ref_3':self.ref_3,
            'ref_4':self.ref_4,
            'ref_5':self.ref_5,
            'ref_6':self.ref_6,
            'ref_grup':self.ref_grup,
            'sonuc':self.sonuc,
            'kontrol':self.kontrol,
            'kategori':self.kategori,
            'sorgu_no':self.sorgu_no,
            'aciklama':self.aciklama,
            'created_at':self.created_at.strftime("%d/%m/%Y %H:%M:%S")
        }

class RaporEnvanter(models.Model):
    saha_no = models.CharField(verbose_name="Saha No", max_length=50, default="")
    user = models.CharField(verbose_name="Kullanıcı Adı", max_length=50, default="")
    seri_no = models.CharField(verbose_name="Seri No", max_length=5000, default="")
    parca_kodu = models.CharField(verbose_name="Parça Kodu", max_length=5000, default="")
    parca_tanimi = models.CharField(verbose_name="Parça Tanımı", max_length=5000, default="")
    bolge = models.CharField(verbose_name="Bölge", max_length=5000, default="")
    miktar = models.IntegerField(verbose_name="Miktar", default=0)
    sayim_fark = models.IntegerField(verbose_name="Sayım Fark", default=0)
    transfer_adet = models.IntegerField(verbose_name="Transfer Adet", default=0)
    sonuc = models.CharField(verbose_name="Sonuç", max_length=9999, default="")
    durum = models.CharField(verbose_name="Durum", max_length=9999, default="")
    lokasyon = models.CharField(verbose_name="Lokasyon", max_length=9999, default="")
    aciklama = models.CharField(verbose_name="Açıklama", max_length=99999, default="")
    rapor = models.ForeignKey(Rapor, on_delete=models.CASCADE, related_name="rapor_envanter")

    class Meta:
        verbose_name = "Terminal Sayım Envanter"
        verbose_name_plural = "Terminal Sayım Envanter"

class RaporReferanslari(models.Model):

    sorgu_no = models.CharField(verbose_name="Sorgu No", max_length=5000, default="")
    ref = models.CharField(verbose_name="Ref", max_length=5000, default="")
    ekipman_parca_kodu = models.CharField(verbose_name="Ekipman Parça Kodu", max_length=5000, default="")
    parca_tanimi = models.CharField(verbose_name="Parça Tanımı", max_length=5000, default="")
    grup_tanimi = models.CharField(verbose_name="Grup Tanımı", max_length=5000, default="")
    rapor_tanimi = models.CharField(verbose_name="Rapor Tanımı", max_length=5000, default="")
    ref_grup = models.CharField(verbose_name="Ref Grup", max_length=5000, default="")
    kategori = models.CharField(verbose_name="Kategori", max_length=5000, default="")
    analiz_no = models.CharField(verbose_name="Analiz No", max_length=5000, default="")

    class Meta:
        verbose_name = "Sorgu Referans"
        verbose_name_plural = "Sorgu Referansları"

class SorguList(models.Model):
    sorgu_no = models.CharField(verbose_name="Sorgu No", max_length=5000, default="")
    kontrol = models.CharField(verbose_name="Kontrol", max_length=5000, default="")
    ref_grup = models.CharField(verbose_name="Ref Grup", max_length=5000, default="")
    kategori = models.CharField(verbose_name="Kategori", max_length=5000, default="")
    check_analyze = models.CharField(verbose_name="Check", max_length=5000, default="")

    class Meta:
        verbose_name = "Sorgu Listesi"
        verbose_name_plural = "Sorgu Listeleri"



class ScorAnaliz(models.Model):
    analiz_no = models.CharField(max_length=255,unique=True)
    ref_min = models.CharField(max_length=400,blank=True,null=True)
    ref_max = models.CharField(max_length=400,blank=True,null=True)
    ref_mix = models.CharField(max_length=400,blank=True,null=True)
    #koşullar. En fazla 4 tane olabilir
    kosul_1 = models.CharField(max_length=400,blank=True,null=True)
    kosul_2 = models.CharField(max_length=400,blank=True,null=True)
    kosul_3 = models.CharField(max_length=400,blank=True,null=True)
    kosul_4 = models.CharField(max_length=400,blank=True,null=True)
    #sonuçlar. Hangi koşul verildiyse ona göre bir koşul verilmesi lazım.
    sonuc_1 = models.CharField(max_length=400,blank=True,null=True)
    sonuc_2 = models.CharField(max_length=400,blank=True,null=True)
    sonuc_3 = models.CharField(max_length=400,blank=True,null=True)
    sonuc_4 = models.CharField(max_length=400,blank=True,null=True)
    #hiçbir koşulun ve durumun gerçekleşmediği durum
    else_case = models.CharField(max_length=400,blank=True,null=True)

    def __str__(self):
        return self.analiz_no


class KontrolRaporu(models.Model):
    parca_kodu = models.CharField(max_length=250,blank=True,null=True)
    parca_tanimi = models.CharField(max_length=250,blank=True,null=True)
    miktar = models.IntegerField(blank=True,null=True)
    sayim_fark = models.IntegerField(default=0)
    sonuc = models.CharField(max_length=250,blank=True,null=True)
    lokasyon = models.CharField(max_length=255,blank=True,null=True)
    aciklama = models.CharField(max_length=255,blank=True,null=True)
    rapor = models.ForeignKey(Rapor,on_delete=models.CASCADE,blank=True,null=True) 


    def __str__(self):
        return self.parca_kodu