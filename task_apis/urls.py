from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('task_create/', views.task_create, name='task_create'),
    path('task_all/', views.task_all, name='task_all'),
    path('task_by_id/<int:pk>/', views.task_by_id, name='task_by_id'),
    path('task_update/<int:pk>/', views.task_update, name='task_update'),
    path('task_delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('member_all/', views.member_all, name='member_all'),
]
