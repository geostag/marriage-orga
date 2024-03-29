# Generated by Django 2.2 on 2020-04-20 12:49

import backend.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0018_document_public'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkoutlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('notes', models.TextField(blank=True, max_length=400)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Coli',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.CharField(blank=True, max_length=400, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to=backend.models.get_upload_filename_document, verbose_name='Bild')),
                ('subcode', models.CharField(blank=True, max_length=16, verbose_name='Anmeldecode')),
                ('guestname', models.CharField(default='-', max_length=100, verbose_name='Gastname')),
                ('checkoutlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Checkoutlist')),
            ],
        ),
    ]
