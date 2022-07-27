from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('investigations', views.getInvestigations),
    path('investigations/<str:pk>/', views.getInvestigation),
    path('investigations/<str:pk>/messages', views.getInvestigationMessages),
]