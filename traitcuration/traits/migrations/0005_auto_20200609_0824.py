# Generated by Django 3.0.6 on 2020-06-09 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traits', '0004_auto_20200604_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ontologyterm',
            name='label',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='ontologyterm',
            name='uri',
            field=models.URLField(blank=True, null=True),
        ),
    ]
