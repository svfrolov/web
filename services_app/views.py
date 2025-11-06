from django.shortcuts import render, get_object_or_404
from datetime import date

def index(request):
    """Главная страница с недвижимостью"""
    services_data = [
        {
            'id': 1,
            'title': 'ЖК Ильинские луга',
            'description': 'Московская область, г. Красногорск, Ильинское шоссе',
            'category': 'Квартира',
            'icon': 'fa-building',
            'area': '54,80',
            'rooms': '1',
            'floor': '8',
            'total_floors': '24',
            'price': '5 500 000'
        },
        {
            'id': 2,
            'title': 'ЖК Ильинские луга',
            'description': 'Московская область, г. Красногорск, Ильинское шоссе',
            'category': 'Квартира',
            'icon': 'fa-building',
            'area': '74,80',
            'rooms': '2',
            'floor': '8',
            'total_floors': '24',
            'price': '7 500 000'
        },
        {
            'id': 3,
            'title': 'ЖК Ильинские луга',
            'description': 'Московская область, г. Красногорск, Ильинское шоссе',
            'category': 'Квартира',
            'icon': 'fa-building',
            'area': '94,80',
            'rooms': '3',
            'floor': '8',
            'total_floors': '24',
            'price': '9 500 000'
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
    """Страница деталей объекта недвижимости"""
    services_data = {
        1: {
            'title': 'ЖК Ильинские луга',
            'description': 'Московская область, г. Красногорск, Ильинское шоссе',
            'category': 'Квартира',
            'icon': 'fa-building',
            'area': '54,80',
            'rooms': '1',
            'floor': '8',
            'total_floors': '24',
            'price': '5 500 000',
            'full_description': 'Просторная однокомнатная квартира в новом жилом комплексе. Светлая и уютная квартира с качественным ремонтом. Развитая инфраструктура района.',
            'location': 'Московская область, г. Красногорск, Ильинское шоссе'
        },
        2: {
            'title': 'ЖК Ильинские луга',
            'description': 'Московская область, г. Красногорск, Ильинское шоссе',
            'category': 'Квартира',
            'icon': 'fa-building',
            'area': '74,80',
            'rooms': '2',
            'floor': '8',
            'total_floors': '24',
            'price': '7 500 000',
            'full_description': 'Просторная двухкомнатная квартира в новом жилом комплексе. Светлая и уютная квартира с качественным ремонтом. Развитая инфраструктура района.',
            'location': 'Московская область, г. Красногорск, Ильинское шоссе'
        },
        3: {
            'title': 'ЖК Ильинские луга',
            'description': 'Московская область, г. Красногорск, Ильинское шоссе',
            'category': 'Квартира',
            'icon': 'fa-building',
            'area': '94,80',
            'rooms': '3',
            'floor': '8',
            'total_floors': '24',
            'price': '9 500 000',
            'full_description': 'Просторная трехкомнатная квартира в новом жилом комплексе. Светлая и уютная квартира с качественным ремонтом. Развитая инфраструктура района.',
            'location': 'Московская область, г. Красногорск, Ильинское шоссе'
        }
    }

    service = services_data.get(id, {})

    context = {
        'service': service,
        'service_id': id,
        'current_date': date.today()
    }
    return render(request, 'services_app/service_detail.html', context)

def order_detail(request, order_id):
    """Страница детального просмотра заявки"""
    # Словарь с данными заявки (заполняется готовыми данными)
    orders_data = {
        1: {
            'id': 1,
            'user_name': 'Иван Иванов',
            'service': {
                'title': 'ЖК Ильинские луга',
                'description': 'Московская область, г. Красногорск, Ильинское шоссе',
                'category': 'Квартира',
                'icon': 'fa-building',
                'area': '54,80',
                'rooms': '1',
                'floor': '8',
                'total_floors': '24',
                'price': '5 500 000'
            },
            'operand': 'Просмотр',
            'result': 'Запись на просмотр',
            'status': 'completed',
            'created_date': '15.09.2025',
            'get_status_display': 'Завершено'
        }
    }

    order = orders_data.get(order_id)
    
    if not order:
        # Если заявка не найдена, можно создать заглушку
        order = {
            'id': order_id,
            'user_name': 'Пользователь',
            'service': {
                'title': 'Объект недвижимости',
                'description': 'Описание объекта',
                'category': 'Категория',
                'icon': 'fa-building',
                'area': '0',
                'rooms': '0',
                'floor': '0',
                'total_floors': '0',
                'price': '0'
            },
            'operand': 'Данные',
            'result': 'Результат',
            'status': 'completed',
            'created_date': date.today().strftime('%d.%m.%Y'),
            'get_status_display': 'Завершено'
        }

    context = {
        'order': order,
        'current_date': date.today()
    }
    return render(request, 'services_app/order_detail.html', context)