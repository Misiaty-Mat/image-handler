# Generated by Django 4.2.6 on 2023-10-15 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_temporarylink'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tier',
            old_name='max_image_height',
            new_name='max_thumbnail_height',
        ),
        migrations.RemoveField(
            model_name='tier',
            name='link_livespan',
        ),
        migrations.AlterField(
            model_name='temporarylink',
            name='token',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='tier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.tier'),
        ),
    ]