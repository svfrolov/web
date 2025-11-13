from minio import Minio
from minio.error import S3Error
from io import BytesIO
from datetime import timedelta

# Настройки клиента MinIO
minio_client = Minio(
    "play.min.io",  # Публичный демо-сервер MinIO
    access_key="Q3AM3UQ867SPQQA43P2F",  # Демо-ключ доступа
    secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",  # Демо-секретный ключ
    secure=True  # Использовать HTTPS
)

# Имя бакета для хранения изображений
BUCKET_NAME = "mstu-buildings-images"

def ensure_bucket_exists():
    """Проверяет существование бакета и создает его при необходимости"""
    try:
        found = minio_client.bucket_exists(BUCKET_NAME)
        if not found:
            minio_client.make_bucket(BUCKET_NAME)
            print(f"Бакет '{BUCKET_NAME}' успешно создан")
        return True
    except S3Error as err:
        print(f"Ошибка при работе с MinIO: {err}")
        return False

def get_image_url(object_name):
    """Получает URL для доступа к изображению"""
    try:
        # Получаем временную ссылку на файл (действительна 7 дней)
        # Используем timedelta вместо целого числа
        url = minio_client.presigned_get_object(
            BUCKET_NAME, 
            object_name, 
            expires=timedelta(days=7)
        )
        return url
    except S3Error as err:
        print(f"Ошибка при получении URL изображения: {err}")
        return None

def upload_image(file_data, object_name):
    """Загружает изображение в MinIO"""
    try:
        ensure_bucket_exists()
        
        # Преобразуем байты в BytesIO объект, если это байты
        if isinstance(file_data, bytes):
            file_data = BytesIO(file_data)
            
        # Определяем content_type на основе расширения файла
        content_type = "image/jpeg"  # По умолчанию
        if object_name.lower().endswith(".png"):
            content_type = "image/png"
        elif object_name.lower().endswith(".gif"):
            content_type = "image/gif"
        
        # Получаем длину файла
        file_data.seek(0, 2)  # Перемещаемся в конец файла
        file_length = file_data.tell()  # Получаем текущую позицию (длину)
        file_data.seek(0)  # Возвращаемся в начало файла
        
        # Загружаем файл в MinIO
        minio_client.put_object(
            BUCKET_NAME,
            object_name,
            file_data,
            length=file_length,
            content_type=content_type
        )
        
        return get_image_url(object_name)
    except S3Error as err:
        print(f"Ошибка при загрузке изображения: {err}")
        return None