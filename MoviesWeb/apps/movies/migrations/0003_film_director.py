# Generated by Django 4.2.11 on 2024-05-14 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_film_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='director',
            field=models.CharField(default='', max_length=50),
        ),
    ]