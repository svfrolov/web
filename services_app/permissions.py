from rest_framework import permissions

class IsModeratorUser(permissions.BasePermission):
    """
    Разрешение только для модераторов.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение для владельца объекта или только чтение для остальных.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешаем GET, HEAD, OPTIONS запросы всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверяем, является ли пользователь владельцем объекта
        return hasattr(obj, 'user') and obj.user == request.user

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Разрешение для аутентифицированных пользователей или только чтение для остальных.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated