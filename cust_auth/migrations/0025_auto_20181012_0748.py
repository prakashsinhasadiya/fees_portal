# Generated by Django 2.0 on 2018-10-12 07:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cust_auth', '0024_auto_20181012_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='feestransactiondetails',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='feestransactiondetails',
            name='u_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]