from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'), 
    path('add/', views.task_add, name='task_add'),  
    path('<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('priority/add/', views.priority_add, name='priority_add'),
    path('category/add/', views.category_add, name='category_add'),
    path('tag/add/', views.tag_add, name='tag_add'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
]
