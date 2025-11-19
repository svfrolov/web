from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .minio_utils import upload_image
import json
import uuid

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