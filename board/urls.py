from django.urls import path
from . import views

app_name = "board"

urlpatterns = [
    path('', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('index/', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('password/', views.password, name="password"),
    path('charts/', views.charts, name="charts"),
    path('tables/', views.tables, name="tables"),
    path('notice/', views.notice, name="notice"),
    path('search/', views.search, name="search"),
]