# Generated by Django 4.2.7 on 2024-01-01 13:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stock_watchlist", "0003_remove_watchlistitems_group_delete_watchlistgroup"),
    ]

    operations = [
        migrations.AddField(
            model_name="watchlistitems",
            name="transactionType",
            field=models.CharField(default="buy", max_length=10),
            preserve_default=False,
        ),
    ]
