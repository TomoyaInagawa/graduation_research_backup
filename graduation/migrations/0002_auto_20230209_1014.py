# Generated by Django 3.2.7 on 2023-02-09 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gourmet',
            name='explanation',
            field=models.TextField(max_length=140, verbose_name='グルメ説明'),
        ),
        migrations.AlterField(
            model_name='place',
            name='explanation',
            field=models.TextField(max_length=140, verbose_name='説明'),
        ),
    ]
