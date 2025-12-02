from django.contrib.auth.models import User

def get_current_user():
    """
    Функция-singleton для получения текущего пользователя.
    В данной реализации пользователь указан константой.
    
    В реальном приложении здесь должна быть логика получения 
    авторизованного пользователя из запроса.
    """
    # Получаем или создаем пользователя с id=1
    user, created = User.objects.get_or_create(
        username='default_user',
        defaults={
            'email': 'default@example.com',
            'first_name': 'Default',
            'last_name': 'User',
            'is_staff': True,
        }
    )
    
    # Если пользователь был создан, устанавливаем пароль
    if created:
        user.set_password('password123')
        user.save()
    
    return user

def get_moderator_user():
    """
    Функция-singleton для получения пользователя-модератора.
    В данной реализации модератор указан константой.
    """
    # Получаем или создаем пользователя-модератора с id=2
    moderator, created = User.objects.get_or_create(
        username='default_moderator',
        defaults={
            'email': 'moderator@example.com',
            'first_name': 'Default',
            'last_name': 'Moderator',
            'is_staff': True,
        }
    )
    
    # Если пользователь был создан, устанавливаем пароль
    if created:
        moderator.set_password('password123')
        moderator.save()
    
    return moderator