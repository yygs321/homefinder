# Generated by Django 5.1.2 on 2024-10-15 07:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("homefind", "0002_remove_realestate_pyeongsu_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="realestate",
            name="category",
            field=models.CharField(
                choices=[
                    ("sell", "sell"),
                    ("lease", "lease"),
                    ("monthlyRent", "monthlyRent"),
                ],
                default="monthlyRent",
                max_length=50,
            ),
        ),
    ]
