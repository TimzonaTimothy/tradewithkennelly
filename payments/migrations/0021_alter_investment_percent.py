# Generated by Django 3.2 on 2024-09-05 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0020_auto_20240806_0631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='percent',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=20, null=True),
        ),
    ]
