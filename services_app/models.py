from django.db import models

class Product(models.Model):
    """Модель для хранения информации о товарах (корпусах МГТУ)"""
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    category = models.CharField(max_length=100, verbose_name="Категория")
    icon = models.CharField(max_length=50, verbose_name="Иконка", default="fa-university")
    area = models.CharField(max_length=20, verbose_name="Площадь (кв.м)")
    rooms = models.CharField(max_length=20, verbose_name="Количество помещений")
    floor = models.CharField(max_length=10, verbose_name="Этаж")
    total_floors = models.CharField(max_length=10, verbose_name="Всего этажей")
    price = models.CharField(max_length=50, verbose_name="Стоимость")
    full_description = models.TextField(verbose_name="Полное описание", blank=True)
    location = models.CharField(max_length=255, verbose_name="Местоположение")
    image_url = models.URLField(verbose_name="URL изображения", blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"