from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, 'board/index.html')
    else:
        return redirect('board:login')

def login(request):
    if request.user.is_authenticated:
        return redirect('board:index')
    if request.method == 'POST':
        username = request.POST.get("userid")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            auth_login(request,user)
            return redirect('board:index')
        else :
            return redirect('board:login')
    return render(request,'board/login.html')

def logout(request):
    auth_logout(request)
    return redirect('board:index')

def register(request):
    return render(request, 'board/register.html')

def password(request):
    return render(request, 'board/password.html')

def charts(request):
    return render(request, 'board/charts.html')

def tables(request):
    return render(request, 'board/tables.html')

def notice(request):
    return render(request, 'board/notice.html')