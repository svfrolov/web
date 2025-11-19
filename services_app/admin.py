from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'has_image')
    list_filter = ('category',)
    search_fields = ('title', 'description')
    
    def has_image(self, obj):
        return bool(obj.image_url)
    
    has_image.boolean = True
    has_image.short_description = "Есть изображение"