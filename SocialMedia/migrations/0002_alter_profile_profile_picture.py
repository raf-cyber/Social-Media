# Generated by Django 5.1.2 on 2024-10-15 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SocialMedia", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile_picture",
            field=models.ImageField(
                default="profile_pics/download.jpg", upload_to="profile_pics/"
            ),
        ),
    ]
