# Generated by Django 3.2.16 on 2022-12-21 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20221221_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='cik',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
