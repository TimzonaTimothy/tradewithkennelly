# Generated by Django 5.0.6 on 2024-08-03 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_crypto_percent_delete_referral_withdrawal_request'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accountbalancecrypto',
            options={'verbose_name': 'Deposit', 'verbose_name_plural': 'Deposits'},
        ),
        migrations.AlterModelOptions(
            name='paymentgatewaycrypto',
            options={'verbose_name': 'Investment', 'verbose_name_plural': 'Investments'},
        ),
        migrations.AlterField(
            model_name='crypto',
            name='investment_type',
            field=models.CharField(blank=True, choices=[('Deposit', 'Deposit'), ('Investment', 'Investment')], max_length=500, null=True),
        ),
    ]
