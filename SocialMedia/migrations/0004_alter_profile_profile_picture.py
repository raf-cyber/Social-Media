# Generated by Django 5.1.2 on 2024-10-17 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SocialMedia", "0003_alter_profile_profile_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile_picture",
            field=models.ImageField(
                blank=True,
                default="profile_pics/default.jpg",
                null=True,
                upload_to="profile_pics",
            ),
        ),
    ]
