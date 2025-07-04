# Generated by Django 5.1.7 on 2025-04-21 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0010_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='thumbnail_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='post_description',
            field=models.TextField(null=True),
        ),
    ]
