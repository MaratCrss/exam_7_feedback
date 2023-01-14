from django.contrib import admin
from webapp.models import Product, Review


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'description', 'image']
    list_display_links = ['id', 'title']
    list_filter = ['title']
    search_fields = ['title', 'category']
    fields = ['title', 'category', 'description', 'image']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'product', 'description', 'grade', 'moderated', 'created_at', 'updated_at']
    list_display_links = ['id', 'author']
    fields = ['description', 'grade', 'moderated']


admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)