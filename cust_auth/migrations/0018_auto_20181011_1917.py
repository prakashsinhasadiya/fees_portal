# Generated by Django 2.0 on 2018-10-11 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cust_auth', '0017_auto_20181011_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feestransactiondetails',
            name='payment_fees_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_dode_fees_type', to='cust_auth.InstituteFees'),
        ),
    ]
