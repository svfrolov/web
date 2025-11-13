from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('service/<int:id>/', views.service_detail, name='service_detail'),
    path('build_request/<int:order_id>/', views.build_request_detail, name='build_request_detail'),
]