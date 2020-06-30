from django.urls import path
from . import views

app_name = "board"

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('password/', views.password, name="password"),
    path('charts/', views.charts, name="charts"),
    path('tables/', views.tables, name="tables"),
    path('notice/', views.notice, name="notice"),
    path('search/', views.search, name="search"),
]