# Generated by Django 3.2.3 on 2021-05-28 11:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0004_auto_20210528_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='photo',
            field=models.FileField(default=django.utils.timezone.now, upload_to=''),
            preserve_default=False,
        ),
    ]
