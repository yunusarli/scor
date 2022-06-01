# Generated by Django 4.0.4 on 2022-05-07 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_tables', '0002_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SahaListesi',
        ),
        migrations.AddField(
            model_name='saha_listesi',
            name='ana_yer_tipi',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='saha_listesi',
            name='status',
            field=models.CharField(choices=[('A', 'Aktif'), ('P', 'Pasif')], default='A', max_length=2),
        ),
        migrations.AlterField(
            model_name='saha_listesi',
            name='saha_tipi',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
