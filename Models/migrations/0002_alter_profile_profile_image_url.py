# Generated by Django 5.1.7 on 2025-03-29 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image_url',
            field=models.URLField(null=True),
        ),
    ]
