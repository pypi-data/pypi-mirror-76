from django.contrib import admin
from ..models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        'slug',
        'created_at',
        'updated_at',
    ]
    search_fields = ['content']
