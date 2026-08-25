from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('responses/', views.responses, name='responses'),
    path('responses/details/<int:id>', views.details, name='details'),
    path('testing/', views.testing, name='testing'),
]