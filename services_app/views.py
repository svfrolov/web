from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.db import connection
from datetime import date
from .models import BuildingObject, TechnicalSupervision, TechnicalSupervisionItem

def index(request):
    """Главная страница со строительными объектами"""
    # Получаем все активные объекты из базы данных через ORM
    building_objects = BuildingObject.objects.filter(is_deleted=False)
    
    # Всегда используем демо-данные для отображения трех объектов
    services_data = [
        {
            'id': 1,
            'title': 'Главный учебный корпус МГТУ',
            'description': 'г. Москва, 2-я Бауманская ул., д. 5, стр. 1',
            'category': 'Учебный корпус',
            'icon': 'fa-university',
            'area': '25000',
            'rooms': '200',
            'floor': '5',
            'total_floors': '5',
            'price': '150 000 000',
            'image_url': '/static/images/building1.jpg'
        },
        {
            'id': 2,
            'title': 'Учебно-лабораторный корпус МГТУ',
            'description': 'г. Москва, Рубцовская наб., д. 2/18',
            'category': 'Лабораторный корпус',
            'icon': 'fa-flask',
            'area': '18000',
            'rooms': '150',
            'floor': '7',
            'total_floors': '7',
            'price': '120 000 000',
            'image_url': '/static/images/building2.jpg'
        },
        {
            'id': 3,
            'title': 'Спортивный комплекс МГТУ',
            'description': 'г. Москва, Госпитальная наб., д. 4/2',
            'category': 'Спорткомплекс',
            'icon': 'fa-dumbbell',
            'area': '12000',
            'rooms': '50',
            'floor': '3',
            'total_floors': '3',
            'price': '80 000 000',
            'image_url': '/static/images/building3.png'
        }
    ]
    
    # Обработка поиска
    search_query = request.GET.get('search', '').strip()
    if search_query:
        filtered_services = []
        for service in services_data:
            if (search_query.lower() in service['title'].lower() or
                search_query.lower() in service['description'].lower() or
                search_query.lower() in service['category'].lower()):
                filtered_services.append(service)
        services_data = filtered_services

    # Получаем текущую заявку пользователя (если она есть)
    current_request = None
    if request.user.is_authenticated:
        current_request = TechnicalSupervision.objects.filter(
            creator=request.user, 
            status='draft'
        ).first()
    
    context = {
        'services': services_data,
        'search_query': search_query,
        'current_request': current_request
    }
    return render(request, 'services_app/index.html', context)

def service_detail(request, id):
    """Страница деталей строительного объекта"""
    # Используем демо-данные для отображения деталей объекта
    services_data = {
        1: {
            'title': 'Главный корпус МГТУ',
            'description': 'г. Москва, 2-я Бауманская ул., д. 5, стр. 1',
            'category': 'Учебный корпус',
            'icon': 'fa-university',
            'area': '25000',
            'rooms': '200',
            'floor': '5',
            'total_floors': '5',
            'price': '150 000 000',
            'full_description': 'Главный корпус МГТУ им. Н.Э. Баумана - историческое здание, в котором расположены основные факультеты и администрация университета. Здесь проходят занятия студентов большинства технических специальностей.',
            'location': 'г. Москва, 2-я Бауманская ул., д. 5, стр. 1',
            'image_url': '/static/images/building1.jpg'
        },
        2: {
            'title': 'Учебно-лабораторный корпус МГТУ',
            'description': 'г. Москва, Рубцовская наб., д. 2/18',
            'category': 'Лабораторный корпус',
            'icon': 'fa-flask',
            'area': '18000',
            'rooms': '150',
            'floor': '7',
            'total_floors': '7',
            'price': '120 000 000',
            'full_description': 'Учебно-лабораторный корпус МГТУ им. Н.Э. Баумана оснащен современным оборудованием для проведения научных исследований и лабораторных работ. Здесь расположены специализированные лаборатории и научные центры.',
            'location': 'г. Москва, Рубцовская наб., д. 2/18',
            'image_url': '/static/images/building2.jpg'
        },
        3: {
            'title': 'Спортивный комплекс МГТУ',
            'description': 'г. Москва, Госпитальная наб., д. 4/2',
            'category': 'Спорткомплекс',
            'icon': 'fa-dumbbell',
            'area': '12000',
            'rooms': '50',
            'floor': '3',
            'total_floors': '3',
            'price': '80 000 000',
            'full_description': 'Спортивный комплекс МГТУ им. Н.Э. Баумана включает в себя бассейн, тренажерные залы, залы для игровых видов спорта и легкой атлетики. Здесь проводятся занятия по физической культуре и тренировки спортивных команд университета.',
            'location': 'г. Москва, Госпитальная наб., д. 4/2',
            'image_url': '/static/images/building3.png'
        }
    }
    
    service = services_data.get(id, services_data.get(1, {}))
    
    # Получаем текущую заявку пользователя (если она есть)
    current_request = None
    if request.user.is_authenticated:
        current_request = TechnicalSupervision.objects.filter(
            creator=request.user, 
            status='draft'
        ).first()

    context = {
        'service': service,
        'service_id': id,
        'current_date': date.today(),
        'current_request': current_request
    }
    return render(request, 'services_app/service_detail.html', context)

@login_required
def add_to_request(request, building_object_id):
    """Добавление объекта в текущую заявку (корзину) через ORM"""
    if request.method == 'POST':
        # Проверяем, существует ли объект в базе данных
        try:
            building_object = BuildingObject.objects.get(id=building_object_id, is_deleted=False)
        except BuildingObject.DoesNotExist:
            # Если объект не найден в базе данных, создаем его на основе демо-данных
            demo_objects = {
                1: {
                    'name': 'Главный учебный корпус МГТУ',
                    'description': 'г. Москва, 2-я Бауманская ул., д. 5, стр. 1',
                    'area': '25000',
                    'floor_count': 5,
                    'location': 'г. Москва, 2-я Бауманская ул., д. 5, стр. 1',
                    'image_url': '/static/images/building1.jpg'
                },
                2: {
                    'name': 'Учебно-лабораторный корпус МГТУ',
                    'description': 'г. Москва, Рубцовская наб., д. 2/18',
                    'area': '18000',
                    'floor_count': 7,
                    'location': 'г. Москва, Рубцовская наб., д. 2/18',
                    'image_url': '/static/images/building2.jpg'
                },
                3: {
                    'name': 'Спортивный комплекс МГТУ',
                    'description': 'г. Москва, Госпитальная наб., д. 4/2',
                    'area': '12000',
                    'floor_count': 3,
                    'location': 'г. Москва, Госпитальная наб., д. 4/2',
                    'image_url': '/static/images/building3.png'
                }
            }
            
            if building_object_id in demo_objects:
                building_object = BuildingObject.objects.create(**demo_objects[building_object_id])
            else:
                messages.error(request, 'Объект не найден')
                return redirect('index')
        
        # Ищем черновики пользователя
        draft_requests = TechnicalSupervision.objects.filter(creator=request.user, status='draft')
        
        if draft_requests.exists():
            # Берем самый последний черновик
            technical_supervision = draft_requests.latest('created_at')
        else:
            # Создаем новый черновик, если нет существующих
            technical_supervision = TechnicalSupervision.objects.create(
                creator=request.user,
                status='draft',
                created_at=timezone.now()
            )
        
        # Пытаемся получить существующий элемент заявки
        request_item, created = TechnicalSupervisionItem.objects.get_or_create(
            technical_supervision=technical_supervision,
            building_object=building_object,
            defaults={
                'quantity': 1,
                'order_number': TechnicalSupervisionItem.objects.filter(technical_supervision=technical_supervision).count() + 1
            }
        )
        
        # Если элемент уже существует, увеличиваем количество
        if not created:
            request_item.quantity += 1
            request_item.save()
        
        messages.success(request, f'Объект "{building_object.name}" добавлен в заявку')
        
        # Перенаправляем на страницу, с которой пришел запрос
        next_url = request.POST.get('next', 'index')
        return redirect(next_url)
    
    return redirect('index')

@login_required
def view_request(request):
    """Просмотр текущей заявки (корзины) через ORM"""
    # Ищем черновики пользователя
    draft_requests = TechnicalSupervision.objects.filter(creator=request.user, status='draft')
    
    if draft_requests.exists():
        # Берем самый последний черновик
        technical_supervision = draft_requests.latest('created_at')
    else:
        # Создаем новый черновик, если нет существующих
        technical_supervision = TechnicalSupervision.objects.create(
            creator=request.user,
            status='draft',
            created_at=timezone.now()
        )
    
    # Получаем все элементы заявки
    request_items = technical_supervision.supervision_items.all().select_related('building_object')
    
    context = {
        'technical_supervision': technical_supervision,
        'request_items': request_items,
        'current_date': date.today()
    }
    return render(request, 'services_app/request.html', context)

@login_required
def delete_request(request, request_id):
    """Логическое удаление заявки через SQL запрос (не ORM)"""
    if request.method == 'POST':
        # Проверяем, что заявка принадлежит текущему пользователю
        technical_supervision = get_object_or_404(TechnicalSupervision, id=request_id, creator=request.user)
        
        # Используем SQL запрос для обновления статуса заявки
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE services_app_technicalsupervision SET status = 'deleted' WHERE id = %s AND creator_id = %s",
                [request_id, request.user.id]
            )
        
        messages.success(request, f'Заявка #{request_id} успешно удалена')
        return redirect('index')
    
    return redirect('index')

def build_request_detail(request, order_id):
    """Страница детального просмотра заявки на технический надзор"""
    # Пытаемся найти заявку в базе данных
    try:
        # Получаем заявку по ID, включая удаленные (чтобы показать информацию о статусе)
        technical_supervision = TechnicalSupervision.objects.get(id=order_id)
        
        # Проверяем, удалена ли заявка
        is_deleted = technical_supervision.status == 'deleted'
        
        # Получаем все элементы заявки
        request_items = technical_supervision.supervision_items.all().select_related('building_object')
        
        # Формируем данные для шаблона
        build_request = {
            'id': technical_supervision.id,
            'user_name': technical_supervision.creator.username,
            'email': technical_supervision.creator.email,
            'phone': technical_supervision.creator.profile.phone if hasattr(technical_supervision.creator, 'profile') else '',
            'payment_method': 'Банковская карта',  # Добавляем способ оплаты
            'operation_type': technical_supervision.construction_type,
            'status': technical_supervision.status,
            'created_date': technical_supervision.created_at.strftime('%d.%m.%Y'),
            'get_status_display': technical_supervision.get_status_display(),
            'is_deleted': is_deleted,  # Добавляем флаг удаления для шаблона
            'items': [
                {
                    'product': {
                        'title': item.building_object.name,
                        'description': item.building_object.description,
                        'category': 'Строительный объект',
                        'icon': 'fa-university',
                        'area': item.building_object.area,
                        'rooms': '~',
                        'floor': '1',
                        'total_floors': item.building_object.floor_count,
                        'price': f'{float(item.building_object.area) * 1000:.2f}',
                        'image_url': item.building_object.image_url or '/static/images/building1.jpg'
                    },
                    'quantity': item.quantity,
                    'order_number': item.order_number
                } for item in request_items
            ],
            'total_price': technical_supervision.estimated_cost
        }
        
        # Добавляем поле service для совместимости с шаблоном из l1
        if request_items:
            first_item = request_items[0]
            build_request['service'] = {
                'title': first_item.building_object.name,
                'image_url': first_item.building_object.image_url or '/static/images/building1.jpg'
            }
        
        # Если заявка удалена, добавляем сообщение
        if is_deleted:
            messages.warning(request, f'Заявка #{order_id} была удалена и отображается только для просмотра.')
        
    except TechnicalSupervision.DoesNotExist:
        # Если заявка не найдена, создаем заглушку
        build_request = {
            'id': order_id,
            'user_name': 'Пользователь',
            'email': 'user@example.com',
            'phone': '+7 (999) 123-45-67',  # Добавляем телефон
            'payment_method': 'Банковская карта',  # Добавляем способ оплаты
            'operation_type': 'Технический надзор',
            'status': 'not_found',  # Особый статус для ненайденных заявок
            'created_date': date.today().strftime('%d.%m.%Y'),
            'get_status_display': 'Не найдена',
            'is_deleted': False,
            'items': [
                {
                    'product': {
                        'title': 'Строительный объект',
                        'description': 'Описание объекта',
                        'category': 'Строительный объект',
                        'icon': 'fa-university',
                        'area': '100',
                        'rooms': '~',
                        'floor': '1',
                        'total_floors': '1',
                        'price': '100000',
                        'image_url': '/static/images/building1.jpg'
                    },
                    'quantity': 1,
                    'order_number': 1
                }
            ],
            'total_price': '0',
            # Добавляем поле service для совместимости с шаблоном из l1
            'service': {
                'title': 'Строительный объект',
                'image_url': '/static/images/building1.jpg'
            }
        }
        
        # Добавляем сообщение об ошибке
        messages.error(request, f'Заявка с ID {order_id} не найдена')

    context = {
        'build_request': build_request,
        'current_date': date.today()
    }
    return render(request, 'services_app/build_request_detail.html', context)