from django.contrib import admin
from .models import BuildingObject, ConstructionRequest, ConstructionRequestItem

@admin.register(BuildingObject)
class BuildingObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'floor_count', 'location', 'is_deleted', 'has_image')
    list_filter = ('is_deleted', 'floor_count')
    search_fields = ('name', 'description', 'location')
    
    def has_image(self, obj):
        return bool(obj.image_url)
    
    has_image.boolean = True
    has_image.short_description = "Есть изображение"

class ConstructionRequestItemInline(admin.TabularInline):
    model = ConstructionRequestItem
    extra = 0

@admin.register(ConstructionRequest)
class ConstructionRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at', 'creator', 'construction_type', 'estimated_cost')
    list_filter = ('status', 'construction_type')
    search_fields = ('creator__username',)
    inlines = [ConstructionRequestItemInline]
    readonly_fields = ('created_at', 'formed_at', 'completed_at')

@admin.register(ConstructionRequestItem)
class ConstructionRequestItemAdmin(admin.ModelAdmin):
    list_display = ('construction_request', 'building_object', 'quantity', 'order_number')
    list_filter = ('order_number',)
    search_fields = ('building_object__name', 'construction_request__id')