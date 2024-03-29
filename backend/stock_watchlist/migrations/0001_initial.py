# Generated by Django 4.2.7 on 2023-12-11 16:56

import datetime
from django.db import migrations, models
import django.db.models.deletion
import stock_watchlist.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("user_profile", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="WatchListGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=25)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user_profile.userprofile",
                    ),
                ),
            ],
            options={
                "verbose_name": "Watchlist Group",
                "verbose_name_plural": "Watchlist Groups",
            },
        ),
        migrations.CreateModel(
            name="WatchListItems",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("watchlist", models.CharField(max_length=25)),
                ("ticker", models.CharField(max_length=20)),
                ("quantity", models.IntegerField()),
                ("price", models.FloatField()),
                ("sector", models.CharField(max_length=100)),
                (
                    "trade_date",
                    models.DateTimeField(default=stock_watchlist.models.default_trade_date),
                ),
                (
                    "created_timestamp",
                    models.DateTimeField(default=datetime.datetime.utcnow),
                ),
                ("comments", models.CharField(max_length=140, null=True)),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="watchlist_items",
                        to="stock_watchlist.watchlistgroup",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user_profile.userprofile",
                    ),
                ),
            ],
            options={
                "verbose_name": "Watchlist Item",
                "verbose_name_plural": "Watchlist Items",
            },
        ),
    ]
