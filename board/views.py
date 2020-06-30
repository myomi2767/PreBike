from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages
from .models import Address, Rent, Recede
# from .forms import ArticleForm
from django.core.paginator import Paginator
import csv, sqlite3



from django.http import JsonResponse

# Create your views here.
def index(request):
    # article = Article.objects.all()
    # 1. Paginator(전체 리스트, 한 페이지당 개수)
    # paginator = Paginator(article, 3)
    # 2. 몇 번째 페이지를 보여줄 것인지 GET으로 가져오기
    # page = request.GET.get('page')
    # 해당하는 페이지의 게시글만 가져오기
    # articles = paginator.get_page(page)
    # context = {
    #     'articles' : articles
    # }
    if request.user.is_authenticated:
        addresses = Address.objects.all()
        rentgu = Address.objects.values_list('rentGu', flat=True).distinct()
        # rentdong = Address.objects.values_list('rentDong', flat=True).distinct()
        stationname = Address.objects.values_list('stationName', flat=True).distinct()
        subpaginator = Paginator(stationname, 10)
        page1 = request.GET.get('page')
        stationname = subpaginator.get_page(page1)
        print("*"*30)
        print(rentgu)
        print("*"*30)
        paginator = Paginator(addresses, 100)
        # 페이지 개수 범위 설정
        page_numbers_range = 10
        max_index = len(paginator.page_range)
        page = request.GET.get('page')
        addresses = paginator.get_page(page)
        # 현재 페이지
        current_page = int(page) if page else 1
        # 시작 인덱스 설정
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        # 끝 인덱스 설정
        end_index = start_index + page_numbers_range
        # print(start_index, end_index)
        if end_index >= max_index:
            end_index = max_index
        paginator_range = paginator.page_range[start_index:end_index]

        context = {
            'addresses' : addresses,
            'rentgu' : rentgu,
            'stationname' : stationname,
            'paginator_range' : paginator_range,
        }
        return render(request, 'board/index.html', context)
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

def search(request):
    selectedgu = request.GET.get('selected')
    print("*"*30)
    print(selectedgu)
    print("*"*30)
    rentdong = Address.objects.filter(rentGu=selectedgu).distinct()
    print("*"*30)
    print(rentdong)
    print("*"*30)
    context = {
        'rentdong' : rentdong
    }
    return JsonResponse(context)