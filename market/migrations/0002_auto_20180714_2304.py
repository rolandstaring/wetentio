# Generated by Django 2.0.7 on 2018-07-14 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='researchrequest',
            old_name='min_par_nr',
            new_name='min_part_nr',
        ),
        migrations.AlterField(
            model_name='researchrequest',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]