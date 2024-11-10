# Generated by Django 5.1.2 on 2024-11-10 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SocialMedia", "0018_card"),
    ]

    operations = [
        migrations.AddField(
            model_name="card",
            name="subtitle",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="card",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="card_images/"),
        ),
        migrations.AlterField(
            model_name="card",
            name="title",
            field=models.CharField(max_length=200),
        ),
    ]