# Generated by Django 5.1.2 on 2024-10-25 10:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SocialMedia", "0011_rename_content_comment_body_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="likes",
            field=models.ManyToManyField(
                related_name="blog_posts", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.DeleteModel(
            name="Like",
        ),
    ]