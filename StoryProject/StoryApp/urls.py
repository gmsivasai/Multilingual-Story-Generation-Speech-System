from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),

    path('login/', views.login_user, name="login"),
    path('login_action/', views.login_action, name="login_action"),

    path('register/', views.register, name="register"),
    path('register_action/', views.register_action, name="register_action"),

    path('logout/', views.logout_user, name="logout"),

    path('generate/', views.generate, name="generate"),
]