from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from services_app.models import TechnicalSupervision, BuildingObject

class Command(BaseCommand):
    help = 'Инициализация групп пользователей и их разрешений'

    def handle(self, *args, **options):
        # Создаем группу модераторов
        moderators_group, created = Group.objects.get_or_create(name='moderators')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "moderators" успешно создана'))
        else:
            self.stdout.write(self.style.SUCCESS('Группа "moderators" уже существует'))
        
        # Получаем ContentType для наших моделей
        supervision_ct = ContentType.objects.get_for_model(TechnicalSupervision)
        building_object_ct = ContentType.objects.get_for_model(BuildingObject)
        
        # Получаем разрешения для модераторов
        permissions = Permission.objects.filter(
            content_type__in=[supervision_ct, building_object_ct],
        )
        
        # Добавляем разрешения в группу модераторов
        moderators_group.permissions.set(permissions)
        self.stdout.write(self.style.SUCCESS('Разрешения успешно добавлены в группу "moderators"'))