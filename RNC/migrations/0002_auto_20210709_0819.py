# Generated by Django 2.2.7 on 2021-07-09 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RNC', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rnc',
            name='Name',
            field=models.CharField(blank=True, max_length=500, null=True, unique=True),
        ),
    ]
