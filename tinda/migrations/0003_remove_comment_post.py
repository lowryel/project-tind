# Generated by Django 4.1 on 2022-08-20 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tinda", "0002_remove_tindadates_name_alter_tindadates_username"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="post",
        ),
    ]
