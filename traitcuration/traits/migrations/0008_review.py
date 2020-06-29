# Generated by Django 3.0.6 on 2020-06-15 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('traits', '0007_auto_20200615_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mapping_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='traits.Mapping')),
                ('reviewer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='traits.User')),
            ],
        ),
    ]