import os
import sys
import requests
from io import BytesIO

# Добавляем путь к проекту в sys.path, чтобы импортировать модули проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем функции для работы с MinIO
from services_app.minio_utils import upload_image, ensure_bucket_exists

def download_image(url):
    """Скачивает изображение по URL"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Ошибка при скачивании изображения: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ошибка при скачивании изображения: {e}")
        return None

def upload_building_images():
    """Загружает изображения корпусов МГТУ в MinIO"""
    # Убеждаемся, что бакет существует
    ensure_bucket_exists()
    
    # Словарь с данными изображений корпусов
    buildings = [
        {
            'name': 'building1.jpg',
            'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Main_building_of_Bauman_Moscow_State_Technical_University.jpg/1280px-Main_building_of_Bauman_Moscow_State_Technical_University.jpg',
            'title': 'Главный корпус МГТУ'
        },
        {
            'name': 'building2.jpg',
            'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/BMSTU_Building_on_Rubtsovskaya_Embankment.jpg/1280px-BMSTU_Building_on_Rubtsovskaya_Embankment.jpg',
            'title': 'Учебно-лабораторный корпус МГТУ'
        },
        {
            'name': 'building3.jpg',
            'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Moscow%2C_Gospitalnaya_Embankment_4-2_%2831321732291%29.jpg/1280px-Moscow%2C_Gospitalnaya_Embankment_4-2_%2831321732291%29.jpg',
            'title': 'Спортивный комплекс МГТУ'
        }
    ]
    
    # Загружаем каждое изображение в MinIO
    for building in buildings:
        print(f"Загрузка изображения: {building['title']}...")
        
        # Скачиваем изображение
        image_data = download_image(building['url'])
        
        if image_data:
            # Загружаем изображение в MinIO
            object_name = building['name']
            url = upload_image(image_data, object_name)
            
            if url:
                print(f"Изображение успешно загружено в MinIO")
                print(f"URL: {url}")
            else:
                print(f"Ошибка при загрузке изображения в MinIO")
        else:
            print(f"Не удалось скачать изображение")
        
        print("-" * 50)

if __name__ == "__main__":
    print("Начинаем загрузку изображений корпусов МГТУ в MinIO...")
    upload_building_images()
    print("Загрузка завершена.")