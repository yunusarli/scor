from celery import shared_task
from .import_export import ImportFile
from django.core.mail import EmailMessage

def send_mail(recipients,message,subject="Dosya Yükleme Bilgilendirmesi"):
    email = EmailMessage(subject=subject, body=message, from_email="rapor@scor-app.com",
                         to=recipients)
    email.send()

@shared_task
def celery_upload_file_task(file,instance,recipients):
    try:
        ImportFile(file,instance).import_to_instance()
        message = "Dosyanız başarı ile yüklendi"
        send_mail(recipients,message)
    except Exception as e:
        message = f" Yükleme esnasında bie hata oluştu Lütfen envanterleri kontrol ediniz. Hata mesajı: {e}"
        send_mail(recipients,message)


