# services_app/serializers.py (часть с вычисляемым полем)
from rest_framework import serializers
from .models import ConstructionRequest

class ConstructionRequestSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ConstructionRequest (заявки на строительство)"""
    creator = UserSerializer(read_only=True)
    moderator = UserSerializer(read_only=True)
    construction_items = ConstructionRequestItemSerializer(many=True, read_only=True)
    
    # Вычисляемое поле для подсчета записей м-м с непустым результатом
    items_with_result_count = serializers.SerializerMethodField()

    class Meta:
        model = ConstructionRequest
        fields = [
            'id', 'status', 'created_at', 'formed_at', 'completed_at',
            'creator', 'moderator', 'construction_type', 'estimated_cost',
            'construction_items', 'items_with_result_count'
        ]

    def get_items_with_result_count(self, obj):
        """
        Вычисляемое поле: количество записей м-м, в которых рассчитываемое поле результата не пустое
        В данном случае, считаем элементы с quantity > 0
        """
        return obj.construction_items.filter(quantity__gt=0).count()