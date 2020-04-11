from django.urls import path
from logo_page import views

urlpatterns = [
    path('', views.main, name="main")
]