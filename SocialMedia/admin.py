from django.contrib import admin
from .models import Post, Comment, Message, Card
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Card)
