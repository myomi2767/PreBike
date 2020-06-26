from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'board/index.html')

def login(request):
    return render(request, 'board/login.html')

def register(request):
    return render(request, 'board/register.html')

def password(request):
    return render(request, 'board/password.html')

def charts(request):
    return render(request, 'board/charts.html')

def tables(request):
    return render(request, 'board/tables.html')