# Generated by Django 2.0 on 2018-10-12 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cust_auth', '0028_remove_feestransactiondetails_u_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feestransactiondetails',
            name='payment_response',
        ),
    ]
