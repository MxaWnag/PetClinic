from django.urls import path
from app01 import views

urlpatterns = [
    path('sign_up', views.sign_up)
]