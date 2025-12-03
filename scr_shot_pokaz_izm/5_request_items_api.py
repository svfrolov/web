# services_app/api_views.py (часть для элементов заявок)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BuildingObject, ConstructionRequest, ConstructionRequestItem
from .serializers import ConstructionRequestItemSerializer
from .utils import get_current_user

@api_view(['POST'])
def add_service_to_request(request):
    """Метод для добавления услуги в заявку"""
    # Получаем текущего пользователя
    current_user = get_current_user()
    
    # Получаем данные из запроса
    building_object_id = request.data.get('building_object_id')
    quantity = request.data.get('quantity', 1)
    order_number = request.data.get('order_number', 1)
    
    if not building_object_id:
        return Response({'error': 'Не указан ID услуги'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Проверяем существование услуги
    try:
        building_object = BuildingObject.objects.get(id=building_object_id, is_deleted=False)
    except BuildingObject.DoesNotExist:
        return Response({'error': 'Услуга не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
    # Ищем или создаем заявку-черновик для текущего пользователя
    draft_request, created = ConstructionRequest.objects.get_or_create(
        creator=current_user,
        status='draft',
        defaults={
            'construction_type': 'Реконструкция'
        }
    )
    
    # Проверяем, не добавлена ли уже эта услуга в заявку
    request_item, created = ConstructionRequestItem.objects.get_or_create(
        construction_request=draft_request,
        building_object=building_object,
        defaults={
            'quantity': quantity,
            'order_number': order_number
        }
    )
    
    if not created:
        # Если услуга уже была в заявке, обновляем количество
        request_item.quantity += quantity
        request_item.save()
    
    serializer = ConstructionRequestItemSerializer(request_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

@api_view(['DELETE'])
def remove_service_from_request(request, request_id, service_id):
    """Метод для удаления услуги из заявки"""
    # Получаем текущего пользователя
    current_user = get_current_user()
    
    # Проверяем существование заявки
    try:
        construction_request = ConstructionRequest.objects.get(id=request_id, creator=current_user)
    except ConstructionRequest.DoesNotExist:
        return Response({'error': 'Заявка не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
    # Проверяем, что заявка в статусе черновик
    if construction_request.status != 'draft':
        return Response({'error': 'Можно удалять услуги только из черновика'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Удаляем услугу из заявки
    try:
        request_item = ConstructionRequestItem.objects.get(
            construction_request=construction_request,
            building_object_id=service_id
        )
        request_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ConstructionRequestItem.DoesNotExist:
        return Response({'error': 'Услуга не найдена в заявке'}, status=status.HTTP_404_NOT_FOUND)