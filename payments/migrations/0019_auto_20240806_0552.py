# Generated by Django 3.1 on 2024-08-06 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0018_crypto_withdrawal_request_wallet_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crypto_withdrawal_request',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='deposit',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='investment',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
