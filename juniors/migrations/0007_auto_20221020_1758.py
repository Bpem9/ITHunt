# Generated by Django 3.2.15 on 2022-10-20 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('juniors', '0006_auto_20221013_1502'),
    ]

    operations = [
        migrations.RenameField(
            model_name='juniorhardskills',
            old_name='hardskill',
            new_name='skill',
        ),
        migrations.RenameField(
            model_name='juniorsoftskills',
            old_name='softskill',
            new_name='skill',
        ),
        migrations.RenameField(
            model_name='juniortools',
            old_name='tool',
            new_name='skill',
        ),
        migrations.AlterUniqueTogether(
            name='juniorhardskills',
            unique_together={('junior', 'skill')},
        ),
        migrations.AlterUniqueTogether(
            name='juniorsoftskills',
            unique_together={('junior', 'skill')},
        ),
        migrations.AlterUniqueTogether(
            name='juniortools',
            unique_together={('junior', 'skill')},
        ),
    ]
