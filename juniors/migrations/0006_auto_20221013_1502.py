# Generated by Django 3.2.15 on 2022-10-13 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('juniors', '0005_junior_sfskills'),
    ]

    operations = [
        migrations.RenameField(
            model_name='junior',
            old_name='descr',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='junior',
            name='sfskills',
        ),
    ]
