# Generated by Django 5.0 on 2024-10-13 02:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ForeignKey(blank=True, help_text='Selecciona una imagen desde la galería de archivos multimedia', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productos_imagenes', to='multimedia.mediafile'),
        ),
    ]
