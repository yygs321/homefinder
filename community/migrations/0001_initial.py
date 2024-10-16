import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserModel",
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
                ("username", models.CharField(max_length=20, verbose_name="유저ID")),
                ("nickname", models.CharField(max_length=20)),
                ("password", models.CharField(max_length=20)),
                ("created_date", models.DateTimeField(verbose_name="date published")),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("board_id", models.AutoField(primary_key=True, serialize=False)),
                ("region_id", models.CharField(max_length=50)),
                ("title", models.CharField(max_length=200)),
                ("content", models.TextField()),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Post",
                "verbose_name_plural": "Posts",
            },
        ),
        migrations.CreateModel(
            name="BoardModel",
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
                ("board_id", models.CharField(max_length=20)),
                ("title", models.CharField(max_length=64, verbose_name="제목")),
                ("contents", models.TextField(verbose_name="내용")),
                ("region_id", models.CharField(max_length=20)),
                ("created_date", models.DateTimeField(verbose_name="date published")),
                (
                    "username",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="community.usermodel",
                    ),
                ),
            ],
        ),
    ]