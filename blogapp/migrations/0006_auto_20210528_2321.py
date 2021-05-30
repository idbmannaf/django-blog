# Generated by Django 3.2.3 on 2021-05-28 17:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0005_author_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='fb_url',
            field=models.URLField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='author',
            name='ld_rul',
            field=models.URLField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='author',
            name='tw_rul',
            field=models.URLField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
