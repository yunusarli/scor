import pandas
from .models import TemporaryExcelKeeper
from database_tables.models import Ekipman,Ekipman_Hareketi, KontrolRaporu

class ImportFile:
    def __init__(self,file,instance) -> None:
        """ Ekipman ve EHT dosyalarının okunması ve ilgili veri 
            tabanına kayıt edilmesi
         """
        #gelen dosya => request.FILES instance olarak
        self.file = file
        #hangi veri tabanına yazılacağı
        self.instance = instance

        file_obj = TemporaryExcelKeeper.objects.create(
            file = self.file
        )
        file_obj.save()

        self.temporary_file = file_obj.file

    def read_file(self):
        """ Dosyayı okumak ve sözlük yapısına çevirmek """
        file = pandas.read_excel(self.temporary_file)
        to_dict = file.to_dict(orient="records")
        return to_dict
    

    
    def import_eht(self):
        records = self.read_file()
        hareket_list = list()
        try:
            for data in records:
                hareket_line = Ekipman_Hareketi(
                islem_no = data['İşlem No'],
                islem_tarihi = data['İşlem Tarihi'],
                parca_kodu = data['Kalem Kodu'],
                parca_tanimi = data['Kalem Adı'],
                islem_miktari = data['İşlem Miktarı'],
                olcum_birimi = data['Ölçüm Birimi'],
                kaynak_yeri = data['Kaynak Stok Yeri'],
                kaynak_adresi = data['Kaynak Stok Adresi'],
                transfer_yeri = data['Transfer Stok Yeri'],
                transfer_adresi = data['Transfer Stok Adresi'],
                islem_tipi = data['İşlem Tipi'],
                kaynak_surec = data['Kaynak Süreç'],
                form_no = data['Form No'],
                kaynak_departman = data['Kaynak Departman'],
                hedef_departman = data['Hedef Departman'],
                hedef_lokasyon = data['Hedef Lokasyon'],
                kullanici_adi = data['Kullanıcı Adı'],
                ekipman_tipi = data['Kalem Tipi'],
                referans = data['Referans']
                )
                hareket_list.append(hareket_line)
            Ekipman_Hareketi.objects.bulk_create(hareket_list,batch_size=99999)

        except KeyError as e:
            print(e)
            return "Error"
        finally:
            self.temporary_file.delete()
        

    
    def import_envanter(self):
        records = self.read_file()
        ekipman_listesi = list()

        try:
            for data in records:
                ekipman = Ekipman(
                parca_kodu=data['Ekipman Parca Kodu'],
                parca_tanimi=data["Parca Tanimi"],
                seri_no=data["Ekipman Seri No"],
                quantity=data["Quantity"],
                saha_tipi=data["Saha Tipi"],
                department=data['Department Code'],
                saha_kodu=data["Saha Kodu"],
                saha_no=data["Saha No"],
                ana_yer_tipi=data["Ana Yer Tipi"],
                teslim_tarihi = data['Teslim Alma Tarihi'],
                sahaya_kurulum_tarihi = data['Sahaya Kurulum Tarihi'],
                ust_ekipman = data['Ustekipman'],
                )
                ekipman_listesi.append(ekipman)
            Ekipman.objects.bulk_create(ekipman_listesi)
        except KeyError:
            return "Error"
        finally:
            self.temporary_file.delete()



    def import_to_instance(self):
        """ Kayıtları ilgili veri tabanına kaydetmek """
        database = self.instance
        records = self.read_file()
        try:
            fields = database._meta.fields
            field_names = [field.name for field in fields]
            record_list = []
            for record in records:
                obj = {}
                record = self.name_converter(record)
                for k in record.keys():
                    if k in field_names:
                        obj[k] = record[k]
                record_list.append(obj)
            instances = [database(**record) for record in record_list]
            database.objects.bulk_create(instances,batch_size=999999)
        except Exception as e:
            print(e)
            return "Error"
        finally:
            self.temporary_file.delete()
    
    @staticmethod
    def name_converter(dictionary:dict) -> dict:
        for k in list(dictionary):
            name = ""
            if len(k.split(" ")) > 1:
                name = "_".join(k.split(" ")).lower()
            else:
                counter = 0
                for m in k:
                    if m.isupper():
                        if counter != 0:
                            name += "_"
                        name += m.lower() 
                        counter += 1
                    else:
                        name += m
            dictionary[name] = dictionary.pop(k)
        return dictionary


