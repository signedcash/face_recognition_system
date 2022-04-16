# Generated by Django 4.0.2 on 2022-03-29 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sfr', '0005_device_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageFace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='images/%Y/%m/%d/')),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('face', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sfr.face')),
            ],
        ),
    ]
