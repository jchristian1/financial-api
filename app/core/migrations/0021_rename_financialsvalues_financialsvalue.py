# Generated by Django 3.2.16 on 2022-12-22 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_financialsvalues'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FinancialsValues',
            new_name='FinancialsValue',
        ),
    ]
