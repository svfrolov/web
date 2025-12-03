# services_app/api_views.py (часть для услуг)
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import BuildingObject
from .serializers import BuildingObjectSerializer
from .minio_utils import upload_image
import uuid

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