from django.urls import path,include
from . import views

urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('findPW/', views.findPW),
    path('getVerificationCode/', views.getVerificationCode),
    path('authenticate/', views.authenticate, name="authenticate"),

]