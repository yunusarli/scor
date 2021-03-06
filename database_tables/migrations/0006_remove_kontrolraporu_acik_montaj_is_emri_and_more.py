# Generated by Django 4.0.4 on 2022-05-20 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database_tables', '0005_rapor_rapor_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='acik_montaj_is_emri',
        ),
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='acik_sokum_is_emri',
        ),
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='durum',
        ),
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='fark',
        ),
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='fark_departmani',
        ),
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='firma',
        ),
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='geldigi_yer',
        ),
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='kalem_kodu',
        ),
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='kalem_tanimi',
        ),
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='kullanici',
        ),
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='lokasyon_kodu',
        ),
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='lokasyon_tanimi',
        ),
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='sayim_adi',
        ),
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='sayim_tarihi',
        ),
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='sistemde_bulundugu_yer',
        ),
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='statu',
        ),
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='statu_aciklamasi',
        ),
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='transfer_edilen_adet',
        ),
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='varlik_seri_no',
        ),
        migrations.RemoveField(
            model_name='kontrolraporu',
            name='zimmet_departmani',
        ),
        migrations.AddField(
            model_name='kontrolraporu',
            name='aciklama',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='kontrolraporu',
            name='lokasyon',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='kontrolraporu',
            name='parca_kodu',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='kontrolraporu',
            name='parca_tanimi',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='kontrolraporu',
            name='rapor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database_tables.rapor'),
        ),
        migrations.AddField(
            model_name='kontrolraporu',
            name='sonuc',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='kontrolraporu',
            name='transfer_adet',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='kontrolraporu',
            name='miktar',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='kontrolraporu',
            name='sayim_fark',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='KontrolBakimRaporu',
        ),
    ]
