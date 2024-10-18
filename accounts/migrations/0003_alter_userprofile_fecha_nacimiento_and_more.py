# Generated by Django 5.0 on 2024-10-13 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_alergias_userprofile_ciudad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, help_text='Ingresa tu fecha de nacimiento', null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True, help_text='Fecha en que te uniste a nosotros'),
        ),
    ]
