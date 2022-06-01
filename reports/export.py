from database_tables.models import Ekipman
from core.settings import BASE_DIR
import os
import xlsxwriter

class ExportExcel:
    """ Excel dosyalarını indirmek amacıyla oluşturulmuş class """

    def get_data(self):
        all_objects = Ekipman.objects.all()
        return all_objects
    
    def file_path(self):
        path=os.path.join(BASE_DIR,\
        'media'+os.sep+'TemporaryExcelKeeper'+\
            os.sep+'demo.xlsx')
        
        dir_path = os.path.join(BASE_DIR,\
        'media'+os.sep+'TemporaryExcelKeeper')

        
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        
        return path

    def generate_scor_excel(self,data_list):
        """ Scor tablosunun verilerini çekmek """
        path = self.file_path()
        workbook = xlsxwriter.Workbook(path)

        worksheet = workbook.add_worksheet()
        titles = [
            "Saha No","Saha Kod","ref1","ref2","ref3","ref4","ref5","ref6",
            "Ref Grup","Sonuc","Kontrol","Kategori","Sorgu No","Açıklama","Tarih"
        ]

        row = 0
        col = 0

        for title in titles:
            worksheet.write(row,col,title)
            col += 1
        
        
        for data in data_list:
            row += 1
            col = 0

            saha_no = data.saha_no
            saha_kodu = data.saha_kodu
            ref_1 = data.ref_1
            ref_2 = data.ref_2
            ref_3 = data.ref_3
            ref_4 = data.ref_4
            ref_5 = data.ref_5
            ref_6 = data.ref_6
            ref_grup = data.ref_grup
            sonuc = data.sonuc
            kontrol = data.kontrol
            kategori = data.kategori
            aciklama = data.aciklama
            created_at = str(data.created_at)



            worksheet.write(row,col,saha_no)
            col += 1
            worksheet.write(row,col,saha_kodu)
            col += 1
            worksheet.write(row,col,ref_1)
            col += 1
            worksheet.write(row,col,ref_2)
            col += 1
            worksheet.write(row,col,ref_3)
            col += 1
            worksheet.write(row,col,ref_4)
            col += 1
            worksheet.write(row,col,ref_5)
            col += 1
            worksheet.write(row,col,ref_6)
            col += 1
            worksheet.write(row,col,ref_grup)
            col += 1
            worksheet.write(row,col,sonuc)
            col += 1
            worksheet.write(row,col,kontrol)
            col += 1
            worksheet.write(row,col,kategori)
            col += 1
            worksheet.write(row,col,aciklama)
            col += 1
            worksheet.write(row,col,created_at)
            
            

        workbook.close()
        return path