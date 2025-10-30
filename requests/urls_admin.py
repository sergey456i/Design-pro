from django.urls import path
from . import views_admin

urlpatterns = [
    path('', views_admin.admin_panel, name='admin_panel'),
    path('status/<int:pk>/', views_admin.change_status, name='change_status'),
    path('categories/', views_admin.manage_categories, name='manage_categories'),
    path('categories/delete/<int:pk>/', views_admin.delete_category, name='delete_category'),
]