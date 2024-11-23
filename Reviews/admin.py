from django.contrib import admin

from.models import Review
# Register your models here.

@admin.register(Review)
class CustomuserAdmin(admin.ModelAdmin):
    list_display = ['id', 'likes', 'dislikes', 'date_posted']