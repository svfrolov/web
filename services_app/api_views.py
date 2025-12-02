from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import BuildingObject, TechnicalSupervision, TechnicalSupervisionItem
from .serializers import (
    BuildingObjectSerializer, TechnicalSupervisionSerializer, 
    TechnicalSupervisionItemSerializer, UserSerializer,
    UserRegistrationSerializer, CartIconSerializer
)
from .utils import get_current_user, get_moderator_user
from .minio_utils import upload_image
import uuid
from django.utils import timezone
from django.db.models import Q, Count
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import django_filters

# Оставляем существующую функцию для совместимости
@csrf_exempt
def upload_product_image(request, product_id=None):
    """
    API-эндпоинт для загрузки изображений товаров через Postman
    
    Принимает POST-запрос с файлом изображения в поле 'image'
    Возвращает URL загруженного изображения
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)
    
    try:
        # Получаем файл из запроса
        image_file = request.FILES.get('image')
        if not image_file:
            return JsonResponse({'error': 'Изображение не предоставлено'}, status=400)
        
        # Генерируем уникальное имя файла
        file_extension = image_file.name.split('.')[-1].lower()
        if product_id:
            # Если указан ID товара, используем его в имени файла
            object_name = f"product_{product_id}_{uuid.uuid4()}.{file_extension}"
        else:
            # Иначе просто используем уникальное имя
            object_name = f"product_{uuid.uuid4()}.{file_extension}"
        
        # Читаем данные файла
        file_data = image_file.read()
        
        # Загружаем изображение в MinIO
        url = upload_image(file_data, object_name)
        
        if url:
            # Здесь можно добавить код для сохранения URL в базу данных
            # Например, если у вас есть модель Product:
            # from .models import Product
            # product = Product.objects.get(id=product_id)
            # product.image_url = url
            # product.save()
            
            return JsonResponse({
                'success': True,
                'image_url': url,
                'object_name': object_name,
                'product_id': product_id
            })
        else:
            return JsonResponse({'error': 'Ошибка при загрузке изображения'}, status=500)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# API для услуг (BuildingObject)
class BuildingObjectViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с услугами (BuildingObject)"""
    queryset = BuildingObject.objects.filter(is_deleted=False)
    serializer_class = BuildingObjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'area', 'floor_count', 'location']
    search_fields = ['name', 'description', 'location']
    ordering_fields = ['name', 'area', 'floor_count']
    
    def perform_destroy(self, instance):
        """Мягкое удаление - помечаем запись как удаленную"""
        instance.is_deleted = True
        instance.save()
    
    @action(detail=True, methods=['post'], url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Метод для загрузки изображения услуги"""
        try:
            building_object = self.get_object()
            
            # Получаем файл из запроса
            image_file = request.FILES.get('image')
            if not image_file:
                return Response({'error': 'Изображение не предоставлено'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Генерируем уникальное имя файла на латинице
            file_extension = image_file.name.split('.')[-1].lower()
            object_name = f"building_object_{building_object.id}_{uuid.uuid4()}.{file_extension}"
            
            # Читаем данные файла
            file_data = image_file.read()
            
            # Загружаем изображение в MinIO
            url = upload_image(file_data, object_name)
            
            if url:
                # Сохраняем URL в базу данных
                building_object.image_url = url
                building_object.save()
                
                return Response({
                    'success': True,
                    'image_url': url,
                    'object_name': object_name,
                    'building_object_id': building_object.id
                })
            else:
                return Response({'error': 'Ошибка при загрузке изображения'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Фильтр для заявок
class TechnicalSupervisionFilter(django_filters.FilterSet):
    """Фильтр для заявок по дате формирования и статусу"""
    formed_at_from = django_filters.DateTimeFilter(field_name='formed_at', lookup_expr='gte')
    formed_at_to = django_filters.DateTimeFilter(field_name='formed_at', lookup_expr='lte')
    
    class Meta:
        model = TechnicalSupervision
        fields = ['status', 'formed_at_from', 'formed_at_to']

# API для заявок (TechnicalSupervision)
class TechnicalSupervisionViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с заявками (TechnicalSupervision)"""
    queryset = TechnicalSupervision.objects.exclude(status='deleted').exclude(status='draft')
    serializer_class = TechnicalSupervisionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TechnicalSupervisionFilter
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
        technical_supervision = self.get_object()
        
        # Проверяем, что заявка в статусе черновик
        if technical_supervision.status != 'draft':
            return Response({'error': 'Только черновик можно сформировать'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Проверяем, что заявка принадлежит текущему пользователю
        if technical_supervision.creator != get_current_user():
            return Response({'error': 'Вы не можете формировать чужие заявки'}, status=status.HTTP_403_FORBIDDEN)
        
        # Проверяем, что в заявке есть услуги
        if technical_supervision.supervision_items.count() == 0:
            return Response({'error': 'Нельзя сформировать пустую заявку'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Формируем заявку
        technical_supervision.submit()
        
        serializer = self.get_serializer(technical_supervision)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put'], url_path='complete')
    def complete_request(self, request, pk=None):
        """Метод для завершения заявки"""
        technical_supervision = self.get_object()
        
        # Проверяем, что заявка в статусе сформирована
        if technical_supervision.status != 'submitted':
            return Response({'error': 'Только сформированную заявку можно завершить'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Завершаем заявку
        technical_supervision.complete(get_moderator_user())
        
        serializer = self.get_serializer(technical_supervision)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put'], url_path='reject')
    def reject_request(self, request, pk=None):
        """Метод для отклонения заявки"""
        technical_supervision = self.get_object()
        
        # Проверяем, что заявка в статусе сформирована
        if technical_supervision.status != 'submitted':
            return Response({'error': 'Только сформированную заявку можно отклонить'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Отклоняем заявку
        technical_supervision.status = 'rejected'
        technical_supervision.moderator = get_moderator_user()
        technical_supervision.completed_at = timezone.now()
        technical_supervision.save()
        
        serializer = self.get_serializer(technical_supervision)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='cart-icon')
    def cart_icon(self, request):
        """Метод для получения иконки корзины"""
        # Получаем текущего пользователя
        current_user = get_current_user()
        
        # Ищем заявку-черновик для текущего пользователя
        try:
            draft_request = TechnicalSupervision.objects.get(creator=current_user, status='draft')
            items_count = draft_request.supervision_items.count()
            
            serializer = CartIconSerializer({
                'request_id': draft_request.id,
                'items_count': items_count
            })
            return Response(serializer.data)
        except TechnicalSupervision.DoesNotExist:
            # Если черновика нет, создаем новый
            draft_request = TechnicalSupervision.objects.create(
                creator=current_user,
                status='draft'
            )
            
            serializer = CartIconSerializer({
                'request_id': draft_request.id,
                'items_count': 0
            })
            return Response(serializer.data)

# API для элементов заявок (TechnicalSupervisionItem)
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
    draft_request, created = TechnicalSupervision.objects.get_or_create(
        creator=current_user,
        status='draft',
        defaults={
            'construction_type': 'Реконструкция'
        }
    )
    
    # Проверяем, не добавлена ли уже эта услуга в заявку
    request_item, created = TechnicalSupervisionItem.objects.get_or_create(
        technical_supervision=draft_request,
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
    
    serializer = TechnicalSupervisionItemSerializer(request_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

@api_view(['DELETE'])
def remove_service_from_request(request, request_id, service_id):
    """Метод для удаления услуги из заявки"""
    # Получаем текущего пользователя
    current_user = get_current_user()
    
    # Проверяем существование заявки
    try:
        technical_supervision = TechnicalSupervision.objects.get(id=request_id, creator=current_user)
    except TechnicalSupervision.DoesNotExist:
        return Response({'error': 'Заявка не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
    # Проверяем, что заявка в статусе черновик
    if technical_supervision.status != 'draft':
        return Response({'error': 'Можно удалять услуги только из черновика'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Удаляем услугу из заявки
    try:
        request_item = TechnicalSupervisionItem.objects.get(
            technical_supervision=technical_supervision,
            building_object_id=service_id
        )
        request_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except TechnicalSupervisionItem.DoesNotExist:
        return Response({'error': 'Услуга не найдена в заявке'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_request_item(request, request_id, service_id):
    """Метод для изменения количества/порядка услуги в заявке"""
    # Получаем текущего пользователя
    current_user = get_current_user()
    
    # Проверяем существование заявки
    try:
        technical_supervision = TechnicalSupervision.objects.get(id=request_id, creator=current_user)
    except TechnicalSupervision.DoesNotExist:
        return Response({'error': 'Заявка не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
    # Проверяем, что заявка в статусе черновик
    if technical_supervision.status != 'draft':
        return Response({'error': 'Можно изменять услуги только в черновике'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Обновляем услугу в заявке
    try:
        request_item = TechnicalSupervisionItem.objects.get(
            technical_supervision=technical_supervision,
            building_object_id=service_id
        )
        
        # Обновляем поля
        quantity = request.data.get('quantity')
        if quantity is not None:
            request_item.quantity = quantity
        
        order_number = request.data.get('order_number')
        if order_number is not None:
            request_item.order_number = order_number
        
        request_item.save()
        
        serializer = TechnicalSupervisionItemSerializer(request_item)
        return Response(serializer.data)
    except TechnicalSupervisionItem.DoesNotExist:
        return Response({'error': 'Услуга не найдена в заявке'}, status=status.HTTP_404_NOT_FOUND)

# API для пользователей
class UserRegistrationView(APIView):
    """API для регистрации пользователей"""
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_profile(request):
    """Метод для получения данных текущего пользователя"""
    user = get_current_user()
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['PUT'])
def update_user_profile(request):
    """Метод для изменения данных текущего пользователя"""
    user = get_current_user()
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    """Метод для аутентификации пользователя"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return Response({'success': True, 'message': 'Успешная аутентификация'})
    return Response({'success': False, 'message': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def user_logout(request):
    """Метод для деавторизации пользователя"""
    logout(request)
    return Response({'success': True, 'message': 'Успешная деавторизация'})