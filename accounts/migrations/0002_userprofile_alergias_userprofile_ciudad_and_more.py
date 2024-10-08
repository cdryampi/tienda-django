# Generated by Django 5.0 on 2024-10-08 02:19

import django.db.models.deletion
import django_countries.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='alergias',
            field=models.ManyToManyField(blank=True, help_text='Indica si tienes alguna alergia alimentaria', to='core.alergia'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='ciudad',
            field=models.CharField(blank=True, help_text='Ciudad donde vives', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='codigo_postal',
            field=models.CharField(blank=True, help_text='Código postal de tu área', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='direccion',
            field=models.CharField(blank=True, help_text='Dirección de residencia (calle y número)', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='fecha_nacimiento',
            field=models.DateField(auto_now=True, help_text='Ingresa tu fecha de nacimiento', null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='fecha_registro',
            field=models.DateTimeField(auto_now=True, help_text='Fecha en que te uniste a nosotros'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='gustos_hamburguesas',
            field=models.ManyToManyField(blank=True, help_text='Selecciona tus hamburguesas favoritas', to='core.hamburguesa'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='pais',
            field=django_countries.fields.CountryField(blank=True, help_text='País de residencia', max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='puntos_fidelidad',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='Puntos acumulados en el programa de fidelidad', null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='suscripcion_boletin',
            field=models.BooleanField(default=False, help_text='Marca esta casilla si deseas recibir nuestro boletín de noticias'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='telefono',
            field=models.CharField(blank=True, help_text='Número de teléfono de contacto', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='foto_perfil',
            field=models.ImageField(blank=True, help_text='Sube una foto de perfil (opcional)', null=True, upload_to='profile_pictures/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(help_text='Usuario asociado a este perfil', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
