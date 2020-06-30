from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import Address, Rent, Recede, Notice, Comment
from .forms import NoticeForm, CommentForm
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
    notices = Notice.objects.all()
    context = {
        'notices' : notices
    }
    return render(request, 'board/notice.html', context)

@login_required
def create(request):
    if request.method == "POST":
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.user = request.user
            notice.save()
            messages.success(request, '게시글 작성 완료!!!!!')
            # return redirect('articles:detail', notice.pk)
            return redirect('board:notice')
        else:
            messages.error(request, '너 잘못된 데이터를 넣었어!!!')
    else:
        form = NoticeForm()
    context = {
        'form': form
    }
    return render(request, 'board/form.html', context)

def detail(request, notice_pk):
    notice = get_object_or_404(Notice, pk=notice_pk)
    comment_form = CommentForm()
    comments = notice.comment_set.all()
    context = {
        'notice' : notice,
        'comment_form' : comment_form,
        'comments' : comments,
    }
    return render(request, 'board/detail.html', context)

@login_required
def update(request, notice_pk):
    notice = get_object_or_404(Notice, pk=notice_pk)
    if notice.user == request.user:
        if request.method == "POST":
            form = NoticeForm(request.POST, request.FILES, instance=notice)
            if form.is_valid():
                notice = form.save()
                return redirect('board:detail', notice.pk)
        else:
            form = NoticeForm(instance=notice)
        context = {
            'form': form
        }
        return render(request, 'board/form.html', context)
    else:
        return redirect('board:detail', notice.pk)

@require_POST
def delete(request, notice_pk):
    if request.user.is_authenticated:
        notice = get_object_or_404(Article, pk=notice_pk)
        if notice.user == request.user:
            notice.delete()
            return redirect('board:notice')
        else:
            return redirect('board:detail', notice_pk.pk)
    return redirect('board:login')

@require_POST
def comment_create(request, notice_pk):
    if request.user.is_authenticated:
        notice = get_object_or_404(Notice, pk=notice_pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.notice = notice
            comment.user = request.user
            comment.save()
            return redirect('board:detail', notice.pk)
        # else:
        #     context = {
        #         'comment_form': comment_form,
        #         'notice': notice
        #     }
        #     return render(request, 'board/detail.html', context)
    else:
        return redirect('board:login')

@require_POST
def comment_delete(request, notice_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.user == request.user:
            comment.delete()
        return redirect('board:detail', notice_pk)
    else:
        return redirect('board:login')

def search(request):
    selectedgu = request.GET.get('rentGu')
    selecteddong = request.GET.get('rentDong')

    rentgu = Address.objects.filter(rentGu=selectedgu)
    rentdong = []
    for data in rentgu:
        rentdong.append(data.rentDong)
    # 중복제거
    rentdong = set(rentdong)    
 
    stationname = []
    if selecteddong != None :
        dong = Address.objects.filter(rentGu=selectedgu, rentDong=selecteddong)
        print(dong)
        for stationdata in dong:
            stationname.append(stationdata.stationName)

    context = {
        'rentdong' : list(rentdong),
        'stationname' : stationname
    }
    return JsonResponse(context)
