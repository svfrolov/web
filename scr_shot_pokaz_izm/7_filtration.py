# services_app/api_views.py (часть для фильтрации)

# Фильтрация для услуг (BuildingObject)
class BuildingObjectViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с услугами (BuildingObject)"""
    queryset = BuildingObject.objects.filter(is_deleted=False)
    serializer_class = BuildingObjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'area', 'floor_count', 'location']
    search_fields = ['name', 'description', 'location']
    ordering_fields = ['name', 'area', 'floor_count']

# Фильтр для заявок по дате и статусу
class ConstructionRequestFilter(django_filters.FilterSet):
    """Фильтр для заявок по дате формирования и статусу"""
    formed_at_from = django_filters.DateTimeFilter(field_name='formed_at', lookup_expr='gte')
    formed_at_to = django_filters.DateTimeFilter(field_name='formed_at', lookup_expr='lte')
    
    class Meta:
        model = ConstructionRequest
        fields = ['status', 'formed_at_from', 'formed_at_to']

# Применение фильтра к API заявок
class ConstructionRequestViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с заявками (ConstructionRequest)"""
    queryset = ConstructionRequest.objects.exclude(status='deleted').exclude(status='draft')
    serializer_class = ConstructionRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ConstructionRequestFilter
    ordering_fields = ['created_at', 'formed_at', 'completed_at']