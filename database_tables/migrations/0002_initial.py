# Generated by Django 4.0.4 on 2022-05-07 07:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('database_tables', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='rapor',
            name='create_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rapor',
            name='updated_user',
            field=models.ManyToManyField(blank=True, related_name='updated_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='parca_kodu_listesi_resimleri',
            name='parca_kodu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database_tables.parca_kodu_listesi'),
        ),
        migrations.AddField(
            model_name='kontrolenvanterscor',
            name='sayim_envanter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database_tables.sayimenvanter'),
        ),
        migrations.AddField(
            model_name='kontrolbakimraporu',
            name='kontrol_rapor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kontrol_rapor', to='database_tables.rapor'),
        ),
        migrations.AddField(
            model_name='kontrolbakimraporu',
            name='referans_rapor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referans_rapor', to='database_tables.rapor'),
        ),
        migrations.AddField(
            model_name='kontrolbakimraporu',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='departmentemails',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database_tables.departmanlar'),
        ),
    ]
