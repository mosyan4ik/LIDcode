# Generated by Django 4.0.5 on 2022-06-22 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainList', '0003_participant_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='name',
            field=models.TextField(verbose_name='Наименование команды'),
        ),
    ]