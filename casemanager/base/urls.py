from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('investigation/<str:pk>/', views.investigation, name="investigation"),
    path('create-investigation/', views.createInvestigation, name="create-investigation"),
    path('update-investigation/<str:pk>', views.updateInvestigation, name="update-investigation"),
    path('delete-investigation/<str:pk>', views.deleteInvestigation, name="delete-investigation"),
]
