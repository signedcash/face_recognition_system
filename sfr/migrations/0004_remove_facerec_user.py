# Generated by Django 4.0.2 on 2022-03-27 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sfr', '0003_facerec'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facerec',
            name='user',
        ),
    ]
