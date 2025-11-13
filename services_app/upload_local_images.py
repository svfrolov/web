import os
import sys
from io import BytesIO

# Добавляем путь к проекту в sys.path, чтобы импортировать модули проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем функции для работы с MinIO
from services_app.minio_utils import ensure_bucket_exists, upload_image

def upload_local_images():
    """Загружает локальные изображения корпусов МГТУ в MinIO"""
    # Убеждаемся, что бакет существует
    ensure_bucket_exists()
    
    # Словарь с данными изображений корпусов
    buildings = [
        {
            'name': 'building1.jpg',  # Изменено расширение с .png на .jpg
            'file_path': 'screenshot/1.jpg',  # Изменено расширение с .png на .jpg
            'title': 'Главный учебный корпус МГТУ'
        },
        {
            'name': 'building2.jpg',  # Изменено расширение с .png на .jpg
            'file_path': 'screenshot/2.jpg',  # Изменено расширение с .png на .jpg
            'title': 'Учебно-лабораторный корпус МГТУ'
        },
        {
            'name': 'building3.png',
            'file_path': 'screenshot/3.png',
            'title': 'Спортивный комплекс МГТУ'
        }
    ]
    
    # Загружаем каждое изображение в MinIO
    for building in buildings:
        print(f"Загрузка изображения: {building['title']}...")
        
        # Проверяем существование файла
        if os.path.exists(building['file_path']):
            # Читаем файл в BytesIO объект
            with open(building['file_path'], 'rb') as f:
                image_data = BytesIO(f.read())
            
            # Загружаем изображение в MinIO
            object_name = building['name']
            url = upload_image(image_data, object_name)
            
            if url:
                print(f"Изображение успешно загружено в MinIO")
                print(f"URL: {url}")
            else:
                print(f"Ошибка при загрузке изображения в MinIO")
        else:
            print(f"Файл не найден: {building['file_path']}")
        
        print("-" * 50)

if __name__ == "__main__":
    print("Начинаем загрузку изображений корпусов МГТУ в MinIO...")
    upload_local_images()
    print("Загрузка завершена.")