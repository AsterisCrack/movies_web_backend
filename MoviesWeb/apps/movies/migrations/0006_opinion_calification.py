# Generated by Django 4.2.11 on 2024-05-14 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_opinion'),
    ]

    operations = [
        migrations.AddField(
            model_name='opinion',
            name='calification',
            field=models.FloatField(default=0),
        ),
    ]