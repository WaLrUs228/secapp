# Generated by Django 4.2.7 on 2023-12-05 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_alter_myuser_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemporaryBanIp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP address')),
                ('attempts', models.IntegerField(default=0, verbose_name='Attempts')),
                ('time_unblock', models.DateTimeField(blank=True, verbose_name='Time')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
            ],
            options={
                'db_table': 'TemporaryBanIp',
            },
        ),
        migrations.AlterField(
            model_name='myuser',
            name='slug',
            field=models.SlugField(),
        ),
    ]
