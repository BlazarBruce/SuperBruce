import json
from blog import models
import functools
import datetime
import requests
from django.conf import settings
from django.http import JsonResponse
from django.contrib import auth # auth模块，可用于登录验证
from django.shortcuts import render,redirect,HttpResponse
from blog.forms import LoginForm, RegForm  # 登录/注册、数据验证表单
from django.views.decorators.csrf import csrf_exempt  # 先不做csrf验证

# 初始展示界面
def hello(request):
        return render(request, 'welcome.html')

# 校验用户是否登录的装饰器
def is_auth(func):
    @functools.wraps(func)
    def inner(request, *args, **kwargs):
        user_info = request.session.get('user_id')
        if not user_info:
            return redirect('/login/')
        return func(request, *args, **kwargs)
    return inner


# 自己生成验证码的登录
def login(request):
    # if request.is_ajax():  # 如果是AJAX请求
    if request.method == "POST":
        # 初始化一个给AJAX返回的数据
        ret = {"status": 0, "msg": ""}
        # 从提交过来的数据中 取到用户名和密码
        username = request.POST.get("username")
        password = request.POST.get("password")
        valid_code = request.POST.get("valid_code")  # 获取用户填写的验证码

        # if valid_code and valid_code.upper() == request.session.get("valid_code", "").upper():
        # 目前只有一张验证码、先写死再程序中
        if valid_code.upper() == "A134Z":
            # 验证码正确
            # 利用auth模块做用户名和密码的校验
            user = models.useInfo.objects.filter(username=username, password=password).first()
            if user:
                # 登录成功将user_id添加到session中
                request.session["user_id"] = user.id
                ret["msg"] = "/index/"
            else:
                # 用户名密码错误
                ret["status"] = 1
                ret["msg"] = "用户名或密码错误！"
        else:
            ret["status"] = 1
            ret["msg"] = "验证码错误"

        return JsonResponse(ret)
    return render(request, "login.html")

@csrf_exempt
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
            # 此处怎样将信息展现给前端用户？？？
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

# 注销界面
def logout(request):
    pass

# 装饰器判断用户是否登录、登录后才可一进入导航界面
@is_auth
def index(request):
    """网站的主界面"""
    # 后端传递数据到前端
    user_id = request.session.get("user_id")
    user_obj = models.useInfo.objects.filter(id=user_id).first()

    return render(request, "index.html", {"obj": user_obj})

#开发计划
@is_auth
def plan(request):
    return render(request, "plan.html")

