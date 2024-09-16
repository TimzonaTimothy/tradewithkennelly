# Generated by Django 5.0.6 on 2024-08-05 21:20

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0010_delete_deposit_delete_investment_deposit_investment_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investment',
            name='user',
        ),
        migrations.CreateModel(
            name='Crypto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True)),
                ('plan', models.CharField(blank=True, max_length=500, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('Wallet_Type', models.CharField(blank=True, max_length=500, null=True)),
                ('detail', models.CharField(blank=True, max_length=500, null=True)),
                ('investment_type', models.CharField(blank=True, choices=[('Deposit', 'Deposit'), ('Investment', 'Investment')], max_length=500, null=True)),
                ('percent', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('added_to_balance', models.BooleanField(default=False, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Investment',
                'verbose_name_plural': 'Investments',
            },
        ),
        migrations.DeleteModel(
            name='Deposit',
        ),
        migrations.DeleteModel(
            name='Investment',
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
    ]
