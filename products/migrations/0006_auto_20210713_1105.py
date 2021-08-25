# Generated by Django 3.2.4 on 2021-07-13 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_stripe_data_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stripe_data',
            old_name='email',
            new_name='model_email',
        ),
        migrations.RenameField(
            model_name='stripe_data',
            old_name='paymment_status',
            new_name='model_paymment_status',
        ),
        migrations.RenameField(
            model_name='stripe_data',
            old_name='price',
            new_name='model_price',
        ),
        migrations.RenameField(
            model_name='stripe_data',
            old_name='transaction_id',
            new_name='model_transaction_id',
        ),
    ]
