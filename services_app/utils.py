from django.contrib.auth.models import User, Group
from rest_framework.exceptions import AuthenticationFailed

def get_current_user(request=None):
    """
    Функция для получения текущего пользователя из запроса.
    
    Args:
        request: HTTP запрос
        
    Returns:
        User: объект пользователя
        
    Raises:
        AuthenticationFailed: если пользователь не аутентифицирован
    """
    if request and request.user and request.user.is_authenticated:
        return request.user
    
    # Для обратной совместимости, если запрос не передан
    if not request:
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
    
    raise AuthenticationFailed('Пользователь не аутентифицирован')

def get_moderator_user(request=None):
    """
    Функция для получения пользователя-модератора из запроса.
    
    Args:
        request: HTTP запрос
        
    Returns:
        User: объект пользователя-модератора
        
    Raises:
        AuthenticationFailed: если пользователь не аутентифицирован или не является модератором
    """
    if request and request.user and request.user.is_authenticated:
        # Проверяем, что пользователь является модератором
        if request.user.groups.filter(name='moderators').exists():
            return request.user
        raise AuthenticationFailed('Пользователь не является модератором')
    
    # Для обратной совместимости, если запрос не передан
    if not request:
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
        
        # Если пользователь был создан, устанавливаем пароль и добавляем в группу модераторов
        if created:
            moderator.set_password('password123')
            moderator.save()
            
            # Создаем группу модераторов, если ее нет
            moderators_group, _ = Group.objects.get_or_create(name='moderators')
            moderator.groups.add(moderators_group)
        
        return moderator
    
    raise AuthenticationFailed('Пользователь не аутентифицирован или не является модератором')

def ensure_moderator_group():
    """
    Функция для создания группы модераторов, если ее нет
    """
    Group.objects.get_or_create(name='moderators')