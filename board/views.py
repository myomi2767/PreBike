from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib import messages
from django.db.models.functions import Substr
from .models import Address, Rent, Recede, Notice, Comment
from .forms import NoticeForm, CommentForm
from django.core.paginator import Paginator
import datetime



from django.http import JsonResponse

# Create your views here.
def index(request):

    if request.user.is_authenticated:
        # Address 모델 DB의 전체 데이터 불러오기
        addresses = Address.objects.all()
        rentgu = Address.objects.values_list('rentGu', flat=True).distinct()
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

def barcharts(request):
    stationNum = request.GET.get('stationNum')
    address = Address.objects.get(stationNum=stationNum)
    print(address)
    print("*"*40)
    print(stationNum)
    print("*"*40)
    a = 7
    rentplacelist = []
    recedeplacelist = []
    for i in range(4):
        if i == 3:
            a = 9
        start_date = datetime.date(2019,11,(i*7+1))
        end_date = datetime.date(2019,11,i*7+a)
        print(start_date, end_date)
        print("*"*40)
        
        # rentplace = Rent.objects.filter(rentTime__contains='2019-11', stationNum=stationNum).order_by('rentTime')
        # recedeplace = Recede.objects.filter(recedeTime__contains='2019-11', restationNum=stationNum).order_by('recedeTime')
        rentplace = Rent.objects.filter(rentTime__range=(start_date, end_date), stationNum=stationNum).order_by('rentTime')
        recedeplace = Recede.objects.filter(recedeTime__range=(start_date, end_date), restationNum=stationNum).order_by('recedeTime')
        rentplacelist.append(rentplace.count())
        recedeplacelist.append(recedeplace.count())
    context = {
        'rentplacelist' : rentplacelist,
        'recedeplacelist' : recedeplacelist,
        'chartStationName' : address.stationName,
    }    
    return JsonResponse(context)

def tables(request):

    return render(request, 'board/tables.html')

def notice(request):
    notices = Notice.objects.all()[::-1]
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
            # return redirect('articles:detail', notice.pk)
            return redirect('board:notice')
        else:
            pass
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
        notice = get_object_or_404(Notice, pk=notice_pk)
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
    
    station = []
    if selecteddong != None :
        dong = Address.objects.filter(rentGu=selectedgu, rentDong=selecteddong)
        for stationdata in dong:
            station.append({'stationname': stationdata.stationName, 'stationnum': stationdata.stationNum})
    
    context = {
        'rentdong' : list(rentdong),
        'station' : station,
    }
    return JsonResponse(context)

def error_404(request):
    return render(request, 'board/404.html')

def error_401(request):
    return render(request, 'board/401.html')

def error_500(request):
    return render(request, 'board/500.html')