# Generated by Django 5.1.3 on 2024-12-11 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stocks", "0002_tradelog"),
    ]

    operations = [
        migrations.AddField(
            model_name="stock",
            name="latest_close",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="stock",
            name="latest_high",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="stock",
            name="latest_low",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="stock",
            name="latest_open",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
    ]
