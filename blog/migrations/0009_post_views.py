# Generated by Django 5.1 on 2024-08-12 23:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0008_remove_comment_email_alter_comment_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="views",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
