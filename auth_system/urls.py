from django.urls import path
from auth_system import views

urlpatterns = [
    path('reg/', views.reg, name="reg"),
    path('auth/', views.auth, name="auth"),
    path('test/', views.test, name="test"),
    path('add_mosru/', views.add_mosru, name="add_mosru"),
    path('detail/<int:user_id>', views.detail, name="detail"),
    path('edit_mosru/', views.edit_mosru, name="edit_mosru"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.logout, name='logout')
]