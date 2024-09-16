# Generated by Django 5.0.6 on 2024-08-03 18:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_alter_accountbalancecrypto_options_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AccountBalanceCrypto',
        ),
        migrations.DeleteModel(
            name='PaymentGatewayCrypto',
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
            ],
            options={
                'verbose_name': 'Deposit',
                'verbose_name_plural': 'Deposits',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('payments.crypto',),
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
            ],
            options={
                'verbose_name': 'Investment',
                'verbose_name_plural': 'Investments',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('payments.crypto',),
        ),
        migrations.RemoveField(
            model_name='crypto',
            name='btc_address',
        ),
        migrations.RemoveField(
            model_name='crypto',
            name='btc_hash_code',
        ),
        migrations.AlterField(
            model_name='crypto',
            name='created_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
