import json
from blog import models
import functools
import datetime
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse

# 初始展示界面
def hello(request):
        return render(request, 'welcome.html')

# 校验用户是否登录的装饰器
def auth(func):
    @functools.wraps(func)
    def inner(request, *args, **kwargs):
        user_info = request.session.get('user_info')
        if not user_info:
            return redirect('/login/')
        return func(request, *args, **kwargs)
    return inner

def login(request):
    """网闸的登录界面"""
    if request.method == "POST":
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        obj = models.useInfo.objects.filter(username=user, password=pwd).first()
        if obj:
            # 该用户已经注册
            # request.session['user_info'] = {'id': obj.id, 'name': obj.username, 'uid': obj.uid}
            return redirect('/index/')
        else:
            # 该用户没有注册、返回注册界面
            return render(request, 'register.html')
    else:
        return render(request, 'login.html')

def register(request):
    """网站注册功能"""
    if request.method == "POST":
        # 获取前端传来的数据
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        email = request.POST.get('email')
        name = request.POST.get('name')
        phone = request.POST.get('tel')
        gender = request.POST.get('gender')
        birthday = request.POST.get('birthday')
        # print(user,pwd,email,name,phone,gender,birthday) # 目前可以拿到前端纯回来发的数据
        # ORM将数据插入数据库、并且返回登录界面
        # 查询是否村子啊该用户
        user_list = models.useInfo.objects.filter(username=user)
        # 判断数据库是否存在改用户
        if user_list :
                error_name = '%s用户名已经存在了' % user
                return  render(request,'register.html')
                # return  render(request,'register.html',{'error_name':error_name})
        # 存储到数据库
        else:
            user = models.useInfo.objects.create(username=user,
                                                 password=pwd,
                                                 email=email,
                                                 name=name,
                                                 phone=phone,
                                                 gender=gender,
                                                 birthday=birthday,
                                                 create_time=datetime.datetime.now())
            user.save()
            return redirect('/login/')
    return render(request, 'register.html')

def index(request):
    """网站的主界面"""
    return render(request, 'index.html')

