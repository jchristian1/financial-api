# Generated by Django 3.2.16 on 2022-12-21 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_company_cik'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statementmetadata',
            name='fiscal_year',
            field=models.CharField(max_length=50),
        ),
    ]
