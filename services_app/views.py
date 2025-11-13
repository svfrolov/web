from django.shortcuts import render, get_object_or_404
from datetime import date

def index(request):
    """Главная страница с корпусами МГТУ"""
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
            'image_url': '/static/images/building1.jpg'  # Прямая ссылка на локальное изображение
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
            'image_url': '/static/images/building2.jpg'  # Прямая ссылка на локальное изображение
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
            'image_url': '/static/images/building3.png'  # Прямая ссылка на локальное изображение
        }
    ]

    # Обработка поиска
    search_query = request.GET.get('search', '').strip()
    filtered_services = services_data

    if search_query:
        filtered_services = []
        for service in services_data:
            if (search_query.lower() in service['title'].lower() or
                search_query.lower() in service['description'].lower() or
                search_query.lower() in service['category'].lower()):
                filtered_services.append(service)

    context = {
        'services': filtered_services,
        'search_query': search_query,
    }
    return render(request, 'services_app/index.html', context)

def service_detail(request, id):
    """Страница деталей корпуса МГТУ"""
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
            'image_url': '/static/images/building1.jpg'  # Прямая ссылка на локальное изображение
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
            'image_url': '/static/images/building2.jpg'  # Прямая ссылка на локальное изображение
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
            'image_url': '/static/images/building3.png'  # Прямая ссылка на локальное изображение
        }
    }

    service = services_data.get(id, {})

    context = {
        'service': service,
        'service_id': id,
        'current_date': date.today()
    }
    return render(request, 'services_app/service_detail.html', context)

def build_request_detail(request, order_id):
    """Страница детального просмотра строительной заявки"""
    # Словарь с данными строительной заявки (заполняется готовыми данными)
    build_requests_data = {
        1: {
            'id': 1,
            'user_name': 'Иван Иванов',
            'service': {
                'title': 'Главный корпус МГТУ',
                'description': 'г. Москва, 2-я Бауманская ул., д. 5, стр. 1',
                'category': 'Учебный корпус',
                'icon': 'fa-university',
                'area': '25000',
                'rooms': '200',
                'floor': '5',
                'total_floors': '5',
                'price': '150 000 000'
            },
            'operand': 'Реконструкция',
            'result': 'Запись на реконструкцию',
            'status': 'completed',
            'created_date': '15.09.2025',
            'get_status_display': 'Завершено'
        }
    }

    build_request = build_requests_data.get(order_id)
    
    if not build_request:
        # Если строительная заявка не найдена, можно создать заглушку
        build_request = {
            'id': order_id,
            'user_name': 'Пользователь',
            'service': {
                'title': 'Корпус МГТУ',
                'description': 'Адрес корпуса',
                'category': 'Тип корпуса',
                'icon': 'fa-university',
                'area': '0',
                'rooms': '0',
                'floor': '0',
                'total_floors': '0',
                'price': '0'
            },
            'operand': 'Реконструкция',
            'result': 'Результат',
            'status': 'completed',
            'created_date': date.today().strftime('%d.%m.%Y'),
            'get_status_display': 'Завершено'
        }

    context = {
        'build_request': build_request,
        'current_date': date.today()
    }
    return render(request, 'services_app/build_request_detail.html', context)