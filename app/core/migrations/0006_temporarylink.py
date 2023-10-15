# Generated by Django 4.2.6 on 2023-10-13 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_tier_user_tier'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemporaryLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=50)),
                ('expiration_time', models.DateTimeField()),
                ('user_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.userimage')),
            ],
        ),
    ]