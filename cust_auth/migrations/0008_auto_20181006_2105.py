# Generated by Django 2.0 on 2018-10-06 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cust_auth', '0007_auto_20181006_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=70),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='first_name',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='last_name',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='dob',
            field=models.DateField(),
        ),
    ]
