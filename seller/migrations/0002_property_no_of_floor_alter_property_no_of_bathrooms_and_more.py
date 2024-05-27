# Generated by Django 4.2.13 on 2024-05-25 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='no_of_floor',
            field=models.IntegerField(blank=True, default=1),
        ),
        migrations.AlterField(
            model_name='property',
            name='no_of_bathrooms',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='property',
            name='no_of_bedrooms',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
