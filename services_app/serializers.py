from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BuildingObject, TechnicalSupervision, TechnicalSupervisionItem

class BuildingObjectSerializer(serializers.ModelSerializer):
    """Сериализатор для модели BuildingObject (строительные услуги)"""
    class Meta:
        model = BuildingObject
        fields = ['id', 'name', 'description', 'area', 'floor_count', 'location', 'image_url']
        read_only_fields = ['id', 'image_url']  # Защита системных полей
    
    def to_representation(self, instance):
        """Исключаем удаленные записи из выдачи"""
        if instance.is_deleted:
            return None
        return super().to_representation(instance)

class TechnicalSupervisionItemSerializer(serializers.ModelSerializer):
    """Сериализатор для модели TechnicalSupervisionItem (элементы заявки)"""
    building_object = BuildingObjectSerializer(read_only=True)
    building_object_id = serializers.PrimaryKeyRelatedField(
        queryset=BuildingObject.objects.filter(is_deleted=False),
        write_only=True,
        source='building_object'
    )

    class Meta:
        model = TechnicalSupervisionItem
        fields = ['id', 'building_object', 'building_object_id', 'quantity', 'order_number']
        read_only_fields = ['id']  # Защита системных полей

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']  # Защита системных полей

class TechnicalSupervisionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели TechnicalSupervision (заявки на технический надзор)"""
    creator = UserSerializer(read_only=True)
    moderator = UserSerializer(read_only=True)
    supervision_items = TechnicalSupervisionItemSerializer(many=True, read_only=True)
    # Вычисляемое поле для подсчета записей м-м с непустым результатом
    items_with_result_count = serializers.SerializerMethodField()

    class Meta:
        model = TechnicalSupervision
        fields = [
            'id', 'status', 'created_at', 'formed_at', 'completed_at',
            'creator', 'moderator', 'construction_type', 'estimated_cost',
            'supervision_items', 'items_with_result_count'
        ]
        read_only_fields = [
            'id', 'status', 'created_at', 'formed_at', 'completed_at',
            'creator', 'moderator', 'estimated_cost'
        ]  # Защита системных полей

    def get_items_with_result_count(self, obj):
        """
        Вычисляемое поле: количество записей м-м, в которых рассчитываемое поле результата не пустое
        В данном случае, считаем элементы с quantity > 0
        """
        return obj.supervision_items.filter(quantity__gt=0).count()
    
    def to_representation(self, instance):
        """Исключаем удаленные записи из выдачи"""
        if instance.status == 'deleted':
            return None
        return super().to_representation(instance)

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей"""
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class CartIconSerializer(serializers.Serializer):
    """Сериализатор для иконки корзины"""
    request_id = serializers.IntegerField()
    items_count = serializers.IntegerField()