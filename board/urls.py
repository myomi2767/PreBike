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
    path('notice/<int:notice_pk>/update', views.update, name="update"),
    path('notice/<int:notice_pk>/delete', views.delete, name="delete"),
    path('notice/<int:notice_pk>/comment_create/', views.comment_create, name="comment_create"),
    path('notice/<int:notice_pk>/comment_delete/<int:comment_pk>/', views.comment_delete, name="comment_delete"),
    path('error_404/', views.error_404, name="error_404"),
    path('error_401/', views.error_401, name="error_401"),
    path('error_500/', views.error_500, name="error_500"),
    path('search/', views.search, name="search"),
]