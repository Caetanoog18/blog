from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_cate')
    list_display_links = ('id', 'name_cate')


admin.site.register(Category, CategoryAdmin)
