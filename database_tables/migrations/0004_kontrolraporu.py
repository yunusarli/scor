# Generated by Django 4.0.4 on 2022-05-16 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_tables', '0003_delete_sahalistesi_saha_listesi_ana_yer_tipi_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='KontrolRaporu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lokasyon_kodu', models.CharField(blank=True, max_length=450, null=True)),
                ('lokasyon_tanimi', models.CharField(blank=True, max_length=450, null=True)),
                ('kullanici', models.CharField(blank=True, max_length=450, null=True)),
                ('firma', models.CharField(blank=True, max_length=450, null=True)),
                ('sayim_adi', models.CharField(blank=True, max_length=450, null=True)),
                ('sayim_tarihi', models.CharField(blank=True, max_length=450, null=True)),
                ('kalem_kodu', models.CharField(blank=True, max_length=450, null=True)),
                ('kalem_tanimi', models.CharField(blank=True, max_length=450, null=True)),
                ('varlik_seri_no', models.CharField(blank=True, max_length=450, null=True)),
                ('miktar', models.CharField(blank=True, max_length=450, null=True)),
                ('sayim_fark', models.CharField(blank=True, max_length=450, null=True)),
                ('transfer_edilen_adet', models.CharField(blank=True, max_length=450, null=True)),
                ('durum', models.CharField(blank=True, max_length=450, null=True)),
                ('statu', models.CharField(blank=True, max_length=450, null=True)),
                ('statu_aciklamasi', models.CharField(blank=True, max_length=450, null=True)),
                ('fark', models.CharField(blank=True, max_length=450, null=True)),
                ('fark_departmani', models.CharField(blank=True, max_length=450, null=True)),
                ('geldigi_yer', models.CharField(blank=True, max_length=450, null=True)),
                ('acik_montaj_is_emri', models.CharField(blank=True, max_length=450, null=True)),
                ('acik_sokum_is_emri', models.CharField(blank=True, max_length=450, null=True)),
                ('sistemde_bulundugu_yer', models.CharField(blank=True, max_length=450, null=True)),
                ('zimmet_departmani', models.CharField(blank=True, max_length=450, null=True)),
            ],
        ),
    ]
