# Generated by Django 5.1.7 on 2025-04-09 02:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0008_alter_profile_address_alter_profile_mobile_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='socialmedia',
            old_name='whatshapp',
            new_name='whatshap',
        ),
    ]
