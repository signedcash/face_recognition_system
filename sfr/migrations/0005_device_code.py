# Generated by Django 4.0.2 on 2022-03-27 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sfr', '0004_remove_facerec_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='code',
            field=models.CharField(default='qwe', max_length=255),
            preserve_default=False,
        ),
    ]
