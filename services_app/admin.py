from django.contrib import admin
from .models import BuildingObject, TechnicalSupervision, TechnicalSupervisionItem

@admin.register(BuildingObject)
class BuildingObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'floor_count', 'location', 'is_deleted', 'has_image')
    list_filter = ('is_deleted', 'floor_count')
    search_fields = ('name', 'description', 'location')
    
    def has_image(self, obj):
        return bool(obj.image_url)
    
    has_image.boolean = True
    has_image.short_description = "Есть изображение"

class TechnicalSupervisionItemInline(admin.TabularInline):
    model = TechnicalSupervisionItem
    extra = 0

@admin.register(TechnicalSupervision)
class TechnicalSupervisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at', 'creator', 'construction_type', 'estimated_cost')
    list_filter = ('status', 'construction_type')
    search_fields = ('creator__username',)
    inlines = [TechnicalSupervisionItemInline]
    readonly_fields = ('created_at', 'formed_at', 'completed_at')

@admin.register(TechnicalSupervisionItem)
class TechnicalSupervisionItemAdmin(admin.ModelAdmin):
    list_display = ('technical_supervision', 'building_object', 'quantity', 'order_number')
    list_filter = ('order_number',)
    search_fields = ('building_object__name', 'technical_supervision__id')