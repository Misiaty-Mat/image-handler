# Generated by Django 4.2.6 on 2023-10-11 15:43

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_userimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='userimage',
            name='image',
            field=models.ImageField(null=True, upload_to=core.models.user_image_file_path),
        ),
    ]