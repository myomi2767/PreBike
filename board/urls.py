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
    path('notice/create/', views.create, name="create"),
    path('notice/<int:notice_pk>/', views.detail, name="detail"),
    path('notice/<int:notice_pk>/comment_create/', views.comment_create, name="comment_create"),
    path('search/', views.search, name="search"),
]