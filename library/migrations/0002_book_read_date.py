# Generated by Django 5.2.1 on 2025-05-29 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='read_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
