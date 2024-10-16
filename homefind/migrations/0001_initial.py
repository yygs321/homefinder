# Generated by Django 5.1.2 on 2024-10-16 07:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Region",
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
                ("region_name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="RealEstate",
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
                ("price", models.FloatField(default=0)),
                ("rent_price", models.FloatField(default=0)),
                (
                    "category",
                    models.CharField(
                        choices=[("매매", "매매"), ("전세", "전세"), ("월세", "월세")],
                        default="월세",
                        max_length=50,
                    ),
                ),
                ("house_name", models.CharField(max_length=50)),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Created Date"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("빌라", "빌라"), ("오피스텔", "오피스텔"), ("원룸", "원룸")],
                        default="원룸",
                        max_length=50,
                    ),
                ),
                (
                    "region",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="real_estates",
                        to="homefind.region",
                    ),
                ),
            ],
        ),
    ]
