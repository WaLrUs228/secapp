# Generated by Django 4.2.7 on 2023-12-04 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_myuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
