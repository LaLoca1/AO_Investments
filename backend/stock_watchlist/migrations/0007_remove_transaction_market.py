# Generated by Django 4.2.7 on 2024-02-01 13:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("stock_watchlist", "0006_transaction_market_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="transaction",
            name="market",
        ),
    ]
