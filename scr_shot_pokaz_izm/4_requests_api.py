# services_app/api_views.py (часть для заявок)
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from .models import ConstructionRequest
from .serializers import ConstructionRequestSerializer, CartIconSerializer
from .utils import get_current_user, get_moderator_user
from django.utils import timezone

# Фильтр для заявок
class ConstructionRequestFilter(django_filters.FilterSet):
    """Фильтр для заявок по дате формирования и статусу"""
    formed_at_from = django_filters.DateTimeFilter(field_name='formed_at', lookup_expr='gte')
    formed_at_to = django_filters.DateTimeFilter(field_name='formed_at', lookup_expr='lte')
    
    class Meta:
        model = ConstructionRequest
        fields = ['status', 'formed_at_from', 'formed_at_to']

# API для заявок (ConstructionRequest)
class ConstructionRequestViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с заявками (ConstructionRequest)"""
    queryset = ConstructionRequest.objects.exclude(status='deleted').exclude(status='draft')
    serializer_class = ConstructionRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ConstructionRequestFilter
    ordering_fields = ['created_at', 'formed_at', 'completed_at']
    
    def perform_create(self, serializer):
        """При создании заявки автоматически устанавливаем создателя"""
        serializer.save(creator=get_current_user(), status='draft')
    
    def perform_destroy(self, instance):
        """Мягкое удаление - изменяем статус на 'deleted'"""
        if instance.status == 'draft':
            instance.status = 'deleted'
            instance.save()
        else:
            return Response({'error': 'Только черновики можно удалять'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['put'], url_path='submit')
    def submit_request(self, request, pk=None):
        """Метод для формирования заявки"""
        construction_request = self.get_object()
        
        # Проверяем, что заявка в статусе черновик
        if construction_request.status != 'draft':
            return Response({'error': 'Только черновик можно сформировать'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Проверяем, что заявка принадлежит текущему пользователю
        if construction_request.creator != get_current_user():
            return Response({'error': 'Вы не можете формировать чужие заявки'}, status=status.HTTP_403_FORBIDDEN)
        
        # Проверяем, что в заявке есть услуги
        if construction_request.construction_items.count() == 0:
            return Response({'error': 'Нельзя сформировать пустую заявку'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Формируем заявку
        construction_request.submit()
        
        serializer = self.get_serializer(construction_request)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put'], url_path='complete')
    def complete_request(self, request, pk=None):
        """Метод для завершения заявки"""
        construction_request = self.get_object()
        
        # Проверяем, что заявка в статусе сформирована
        if construction_request.status != 'submitted':
            return Response({'error': 'Только сформированную заявку можно завершить'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Завершаем заявку
        construction_request.complete(get_moderator_user())
        
        serializer = self.get_serializer(construction_request)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='cart-icon')
    def cart_icon(self, request):
        """Метод для получения иконки корзины"""
        # Получаем текущего пользователя
        current_user = get_current_user()
        
        # Ищем заявку-черновик для текущего пользователя
        try:
            draft_request = ConstructionRequest.objects.get(creator=current_user, status='draft')
            items_count = draft_request.construction_items.count()
            
            serializer = CartIconSerializer({
                'request_id': draft_request.id,
                'items_count': items_count
            })
            return Response(serializer.data)
        except ConstructionRequest.DoesNotExist:
            # Если черновика нет, создаем новый
            draft_request = ConstructionRequest.objects.create(
                creator=current_user,
                status='draft'
            )
            
            serializer = CartIconSerializer({
                'request_id': draft_request.id,
                'items_count': 0
            })
            return Response(serializer.data)