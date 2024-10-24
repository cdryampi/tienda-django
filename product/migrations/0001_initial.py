# Generated by Django 5.0 on 2024-10-22 16:53

import django.db.models.deletion
import django.utils.timezone
import django_ckeditor_5.fields
import parler.fields
import parler.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        ('core', '0001_initial'),
        ('multimedia', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_titulo', models.CharField(blank=True, help_text='Metatitulo para el Seo', max_length=255, null=True, verbose_name='Metatitulo')),
                ('meta_descripcion', models.CharField(blank=True, help_text='Metadescripción para el Seo', max_length=255, null=True, verbose_name='Metadescripcion')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('en_stock', models.BooleanField(default=True)),
                ('alergias', models.ManyToManyField(blank=True, help_text='Alergias relacionadas con el producto', to='core.allergy')),
                ('categoria', models.ForeignKey(help_text='Categoría a la que pertenece el producto', on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='common.category')),
                ('created_by', models.ForeignKey(blank=True, help_text='Usuario que creó el objeto', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('documento', models.ForeignKey(blank=True, help_text='Sube una nota o documento relevante asociado con el producto', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productos_documentos', to='multimedia.documentfile')),
                ('hamburguesa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='core.burgertype')),
                ('imagen', models.ForeignKey(blank=True, help_text='Selecciona una imagen desde la galería de archivos multimedia', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productos_imagenes', to='multimedia.mediafile')),
                ('tags', models.ManyToManyField(blank=True, help_text='Etiquetas relacionadas con el producto', related_name='productos', to='common.tag')),
                ('updated_by', models.ForeignKey(blank=True, help_text='Usuario que actualizó por última vez el objeto', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProductTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('titulo', models.CharField(max_length=100, verbose_name='Título')),
                ('descripcion', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Descripción')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='product.product')),
            ],
            options={
                'verbose_name': 'product Translation',
                'db_table': 'product_product_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]