# Generated by Django 5.1.2 on 2024-11-08 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SocialMedia", "0015_remove_profile_profile_picture_profile_profile_img"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="profile_img",
        ),
        migrations.AddField(
            model_name="profile",
            name="profile_picture",
            field=models.ImageField(
                blank=True,
                default="images/default.png",
                null=True,
                upload_to="profile_pics/",
            ),
        ),
    ]