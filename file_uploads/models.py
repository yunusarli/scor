from django.db import models

class TemporaryExcelKeeper(models.Model):
    file = models.FileField(upload_to="temporary_excels/")

    def __str__(self):
        return self.file.name
    
    def get_file_name(self):
        return self.file.name