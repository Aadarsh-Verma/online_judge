# Generated by Django 3.1.7 on 2021-03-29 04:21

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('judge', '0004_contest_participants'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Participants',
            new_name='Participant',
        ),
    ]
