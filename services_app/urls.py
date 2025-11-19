from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('', views.index, name='index'),
    path('service/<int:id>/', views.service_detail, name='service_detail'),
    path('build_request/<int:order_id>/', views.build_request_detail, name='build_request_detail'),
    
    # API эндпоинты для работы с изображениями
    path('api/upload-image/', api_views.upload_product_image, name='upload_image'),
    path('api/products/<int:product_id>/upload-image/', api_views.upload_product_image, name='upload_product_image'),
]