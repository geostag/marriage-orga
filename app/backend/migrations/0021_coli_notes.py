# Generated by Django 2.2 on 2020-04-20 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0020_auto_20200420_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='coli',
            name='notes',
            field=models.TextField(blank=True, max_length=400),
        ),
    ]
