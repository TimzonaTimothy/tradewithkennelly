# Generated by Django 5.0.6 on 2024-08-03 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_crypto_investment_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crypto',
            old_name='order_number',
            new_name='transaction_id',
        ),
        migrations.RemoveField(
            model_name='crypto',
            name='is_ordered',
        ),
        migrations.AlterField(
            model_name='crypto',
            name='investment_type',
            field=models.CharField(blank=True, choices=[('Payment Gateway', 'Payment Gateway'), ('Account Balance', 'Account Balance')], default='Payment Gateway', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='crypto',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20, null=True),
        ),
    ]
