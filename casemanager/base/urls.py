from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('investigation/<str:pk>/', views.investigation, name="investigation"),
]
