# Generated by Django 3.1.7 on 2021-03-28 14:46

import authy.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('bio', models.CharField(blank=True, max_length=100)),
                ('college', models.CharField(blank=True, max_length=100)),
                ('picture', models.ImageField(blank=True, upload_to=authy.models.user_directory_path)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
