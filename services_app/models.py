from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BuildingObject(models.Model):
    """Модель для хранения информации о строительных объектах (услугах)"""
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    is_deleted = models.BooleanField(default=False, verbose_name="Удален")
    image_url = models.URLField(verbose_name="URL изображения", blank=True, null=True)
    # Поля по строительной тематике
    area = models.CharField(max_length=20, verbose_name="Площадь (кв.м)")
    floor_count = models.IntegerField(verbose_name="Количество этажей", default=1)
    location = models.CharField(max_length=255, verbose_name="Местоположение")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Строительный объект"
        verbose_name_plural = "Строительные объекты"

class ConstructionRequest(models.Model):
    """Модель для хранения заявок на строительство"""
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('deleted', 'Удален'),
        ('submitted', 'Сформирован'),
        ('completed', 'Завершен'),
        ('rejected', 'Отклонен'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='construction_requests', verbose_name="Создатель")
    formed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата формирования")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата завершения")
    moderator = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='moderated_requests', 
        null=True, 
        blank=True, 
        verbose_name="Модератор"
    )
    # Поля по строительной тематике
    construction_type = models.CharField(max_length=50, verbose_name="Тип строительства", default="Реконструкция")
    estimated_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Расчетная стоимость")
    
    def __str__(self):
        return f"Заявка на строительство #{self.id} ({self.get_status_display()})"
    
    class Meta:
        verbose_name = "Заявка на строительство"
        verbose_name_plural = "Заявки на строительство"
        
    def calculate_estimated_cost(self):
        """Метод для расчета расчетной стоимости заявки"""
        total = 0
        for item in self.construction_items.all():
            # Расчет стоимости на основе площади объекта и количества
            base_cost = float(item.building_object.area) * 1000  # Примерная стоимость за кв.м
            total += base_cost * item.quantity
        return total
    
    def submit(self):
        """Метод для формирования заявки"""
        if self.status == 'draft':
            self.status = 'submitted'
            self.formed_at = timezone.now()
            self.save()
    
    def complete(self, moderator):
        """Метод для завершения заявки"""
        if self.status == 'submitted':
            self.status = 'completed'
            self.completed_at = timezone.now()
            self.moderator = moderator
            # Рассчитываем стоимость при завершении
            self.estimated_cost = self.calculate_estimated_cost()
            self.save()

class ConstructionRequestItem(models.Model):
    """Модель для связи многие-ко-многим между заявками и строительными объектами"""
    construction_request = models.ForeignKey(ConstructionRequest, on_delete=models.PROTECT, related_name='construction_items', verbose_name="Заявка")
    building_object = models.ForeignKey(BuildingObject, on_delete=models.PROTECT, related_name='request_items', verbose_name="Строительный объект")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    order_number = models.PositiveIntegerField(default=1, verbose_name="Порядковый номер")
    
    def __str__(self):
        return f"{self.building_object.name} ({self.quantity} шт.) в заявке #{self.construction_request.id}"
    
    class Meta:
        verbose_name = "Элемент заявки на строительство"
        verbose_name_plural = "Элементы заявок на строительство"
        # Составной уникальный ключ
        unique_together = ('construction_request', 'building_object')