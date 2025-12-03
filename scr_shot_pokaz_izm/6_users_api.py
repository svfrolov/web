# services_app/api_views.py (часть для пользователей)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer, UserRegistrationSerializer
from .utils import get_current_user

class UserRegistrationView(APIView):
    """API для регистрации пользователей"""
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_profile(request):
    """Метод для получения данных текущего пользователя"""
    user = get_current_user()
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['PUT'])
def update_user_profile(request):
    """Метод для изменения данных текущего пользователя"""
    user = get_current_user()
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    """Метод для аутентификации пользователя"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return Response({'success': True, 'message': 'Успешная аутентификация'})
    return Response({'success': False, 'message': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def user_logout(request):
    """Метод для деавторизации пользователя"""
    logout(request)
    return Response({'success': True, 'message': 'Успешная деавторизация'})