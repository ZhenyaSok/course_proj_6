from django.contrib import admin

from materials.models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'views_count')
    list_filter = ('is_published',)
    search_fields = ('title',)
