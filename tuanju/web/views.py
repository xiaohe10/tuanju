# This Python file uses the following encoding: utf-8
# author : xiaoh16@gmail.com

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm,authenticate
from django.contrib.auth import login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from web.models import *
from django.contrib import messages
from django.views.decorators.cache import cache_page
# Create your views here.
def hello(request):
    return render(request,'hello.html',locals())
type_title = {
    'organizations':'校级组织',
    'departments':'院系所',
    'zhibu':'团支部',
    'surround':'清华周边',
    'all':'所有'

}
#@cache_page(60*60*6)
def get_cubes(request):
    t = tuanju()
    if request.GET.has_key('tuanju_type'):
        tuanju_type = request.GET['tuanju_type']
    else:
        tuanju_type='all'
    key = None
    if request.GET.has_key('key'):
        key = request.GET['key']
        if key == '':
            key = None
    list = t.list(tuanju_type=tuanju_type,key=key,target='show')
    title = type_title[tuanju_type]
    return render(request,'cube.html',locals())

@login_required(login_url='/login')
def organizations(request):
    t = tuanju()
    tuanju_type = 'organizations'
    page = tuanju_type
    list = t.list(tuanju_type)
    return render(request, 'table.html',locals())
@login_required(login_url='/login')
def departments(request):
    t = tuanju()
    tuanju_type = 'departments'
    page = tuanju_type
    list = t.list(tuanju_type)
    return render(request, 'table.html',locals())

@login_required(login_url='/login')
def zhibu(request):
    t = tuanju()
    tuanju_type = 'zhibu'
    page = tuanju_type
    list = t.list(tuanju_type)
    return render(request, 'table.html',locals())

@login_required(login_url='/login')
def surround(request):
    t = tuanju()
    tuanju_type = 'surround'
    page = tuanju_type
    list = t.list(tuanju_type)
    return render(request, 'table.html',locals())


@csrf_exempt
def my_login(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/organizations')
            else:
                login_errors = '用户未激活'
        else:
            login_errors = '用户名或密码不正确'

    else:
        login_form = AuthenticationForm
    return render(request,'login.html',locals())

def my_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')
def re_order(tuanju_type):
    list = tuanju.objects.filter(tuanju_type=tuanju_type).order_by('order')
    count = 1
    for l in list:
        if l.order != count:
            l.order = count
            l.save()
        count += 1
@csrf_exempt
@login_required(login_url='/login')
def add(request):
    try:
        name = request.POST['name']
        url = request.POST['url']
        tuanju_type = request.POST['tuanju_type']
        count = tuanju.objects.filter(tuanju_type=tuanju_type).count()
        t = tuanju(name = name,url = url,tuanju_type = tuanju_type,order=count+1)
        if request.FILES.has_key('icon'):
            t.icon = request.FILES['icon']
        t.save()
        messages.success(request,'添加成功')
    except:
        messages.error(request,'添加失败')
    return HttpResponseRedirect('/'+tuanju_type)
@login_required(login_url='/login')
def delete(request):

    id = request.GET['id']
    tuanju_type = request.GET['tuanju_type']
    try:
        id = int(id)
        t = tuanju.objects.get(id = id)
        t.delete()
        re_order(t.tuanju_type)
        messages.success(request,'删除成功')
    except:
        messages.error(request,'删除失败')

    return HttpResponseRedirect('/'+tuanju_type)
@login_required(login_url='/login')
def modify(request):
    try:
        id = request.POST['id']
        name = request.POST['name']
        url = request.POST['url']
        tuanju_type = request.POST['tuanju_type']
        t = tuanju.objects.get(id = int(id))
        t.name = name
        t.url = url
        t.tuanju_type = tuanju_type
        if request.FILES.has_key('icon'):
            t.icon = request.FILES['icon']
        t.save()
        messages.success(request,'修改成功')
    except:
        messages.error(request,'修改失败')

    return HttpResponseRedirect('/'+tuanju_type)
@login_required(login_url='/login')
def up(request):
    try:
        id = request.GET['id']
        tuanju_type = request.GET['tuanju_type']
        t = tuanju.objects.get(id = int(id))
        if t.order >1:
            t1 = tuanju.objects.get(order = t.order-1,tuanju_type = tuanju_type)
            t1.order = t.order
            t.order -= 1
            t.save()
            t1.save()
            messages.success(request,'上调成功')
        else:
            messages.success(request,'已经处于最顶层')
    except:
        messages.error(request,'上调失败')
    return HttpResponseRedirect('/'+tuanju_type)
@login_required(login_url='/login')
def down(request):
    try:
        id = request.GET['id']
        tuanju_type = request.GET['tuanju_type']
        t = tuanju.objects.get(id = int(id))
        count = tuanju.objects.filter(tuanju_type = tuanju_type).count()
        if t.order < count:
            t1 = tuanju.objects.get(order = t.order+1,tuanju_type = tuanju_type)
            t1.order = t.order
            t.order += 1
            t.save()
            t1.save()
            messages.success(request,'下调成功')
        else:
            messages.success(request,'已经处于最底层')
    except:
        messages.error(request,'下调失败')
    return HttpResponseRedirect('/'+tuanju_type)
