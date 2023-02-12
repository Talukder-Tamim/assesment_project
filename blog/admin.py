from django.contrib import admin
from .models import UserAccount, Post, Comment

admin.site.register(UserAccount)
admin.site.register(Post)
admin.site.register(Comment)
