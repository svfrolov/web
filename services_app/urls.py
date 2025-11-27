from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views

# Создаем роутер для API
router = DefaultRouter()
router.register(r'services', api_views.BuildingObjectViewSet, basename='service')
router.register(r'requests', api_views.ConstructionRequestViewSet, basename='request')

urlpatterns = [
    # Стандартные маршруты для веб-интерфейса
    path('', views.index, name='index'),
    path('service/<int:id>/', views.service_detail, name='service_detail'),
    path('build_request/<int:order_id>/', views.build_request_detail, name='build_request_detail'),
    path('add-to-request/<int:building_object_id>/', views.add_to_request, name='add_to_request'),
    path('technical_supervision/', views.view_request, name='view_request'),
    path('delete-request/<int:request_id>/', views.delete_request, name='delete_request'),
    
    # API маршруты
    path('api/', include(router.urls)),
    
    # Маршруты для работы с изображениями
    path('api/upload-image/', api_views.upload_product_image, name='upload_image'),
    path('api/products/<int:product_id>/upload-image/', api_views.upload_product_image, name='upload_product_image'),
    
    # API для элементов заявок
    path('api/requests/add-service/', api_views.add_service_to_request, name='add_service_to_request'),
    path('api/requests/<int:request_id>/services/<int:service_id>/', api_views.remove_service_from_request, name='remove_service_from_request'),
    path('api/requests/<int:request_id>/services/<int:service_id>/update/', api_views.update_request_item, name='update_request_item'),
    
    # API для иконки корзины
    path('api/cart-icon/', api_views.ConstructionRequestViewSet.as_view({'get': 'cart_icon'}), name='cart_icon'),
    
    # API для пользователей
    path('api/users/register/', api_views.UserRegistrationView.as_view(), name='user_registration'),
    path('api/users/profile/', api_views.get_user_profile, name='user_profile'),
    path('api/users/profile/update/', api_views.update_user_profile, name='update_user_profile'),
    path('api/users/login/', api_views.user_login, name='user_login'),
    path('api/users/logout/', api_views.user_logout, name='user_logout'),
]