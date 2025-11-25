from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('', views.index, name='index'),
    path('service/<int:id>/', views.service_detail, name='service_detail'),
    path('build_request/<int:order_id>/', views.build_request_detail, name='build_request_detail'),
    
    # Новые маршруты для работы с заявками
    path('add-to-request/<int:building_object_id>/', views.add_to_request, name='add_to_request'),
    path('technical_supervision/', views.view_request, name='view_request'),  # Изменено с 'request/' на 'technical_supervision/'
    path('delete-request/<int:request_id>/', views.delete_request, name='delete_request'),
    
    # API эндпоинты для работы с изображениями
    path('api/upload-image/', api_views.upload_product_image, name='upload_image'),
    path('api/products/<int:product_id>/upload-image/', api_views.upload_product_image, name='upload_product_image'),
]