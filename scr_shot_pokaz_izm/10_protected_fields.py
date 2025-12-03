# services_app/serializers.py (часть с защитой системных полей)
from rest_framework import serializers
from .models import BuildingObject, ConstructionRequest, ConstructionRequestItem

class BuildingObjectSerializer(serializers.ModelSerializer):
    """Сериализатор для модели BuildingObject (строительные услуги)"""
    class Meta:
        model = BuildingObject
        fields = ['id', 'name', 'description', 'area', 'floor_count', 'location', 'image_url']
        read_only_fields = ['id', 'image_url']  # Защита системных полей

class ConstructionRequestItemSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ConstructionRequestItem (элементы заявки)"""
    building_object = BuildingObjectSerializer(read_only=True)
    building_object_id = serializers.PrimaryKeyRelatedField(
        queryset=BuildingObject.objects.filter(is_deleted=False),
        write_only=True,
        source='building_object'
    )

    class Meta:
        model = ConstructionRequestItem
        fields = ['id', 'building_object', 'building_object_id', 'quantity', 'order_number']
        read_only_fields = ['id']  # Защита системных полей

class ConstructionRequestSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ConstructionRequest (заявки на строительство)"""
    creator = UserSerializer(read_only=True)
    moderator = UserSerializer(read_only=True)
    construction_items = ConstructionRequestItemSerializer(many=True, read_only=True)
    items_with_result_count = serializers.SerializerMethodField()

    class Meta:
        model = ConstructionRequest
        fields = [
            'id', 'status', 'created_at', 'formed_at', 'completed_at',
            'creator', 'moderator', 'construction_type', 'estimated_cost',
            'construction_items', 'items_with_result_count'
        ]
        read_only_fields = [
            'id', 'status', 'created_at', 'formed_at', 'completed_at',
            'creator', 'moderator', 'estimated_cost'
        ]  # Защита системных полей