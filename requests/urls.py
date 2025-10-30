from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('create/', views.create_request, name='create_request'),
    path('delete/<int:pk>/', views.delete_request, name='delete_request'),
]