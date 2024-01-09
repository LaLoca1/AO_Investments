# Generated by Django 4.2.7 on 2024-01-09 15:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stock_watchlist", "0005_transaction_delete_watchlistitems"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="market",
            field=models.CharField(
                choices=[("UK", "United Kingdom"), ("US", "United States")],
                default="US",
                max_length=2,
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="created_timestamp",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="quantity",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="trade_date",
            field=models.DateTimeField(),
        ),
    ]