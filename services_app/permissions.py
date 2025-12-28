from rest_framework import permissions

class IsModeratorUser(permissions.BasePermission):
    """
    Разрешение только для модераторов.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='moderators').exists()

class IsOwnerOrModerator(permissions.BasePermission):
    """
    Разрешение для владельца объекта или модератора.
    """
    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь модератором
        is_moderator = request.user.groups.filter(name='moderators').exists()
        
        # Проверяем, является ли пользователь владельцем объекта
        is_owner = hasattr(obj, 'creator') and obj.creator == request.user
        
        return is_owner or is_moderator

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Разрешение для аутентифицированных пользователей или только чтение для остальных.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated