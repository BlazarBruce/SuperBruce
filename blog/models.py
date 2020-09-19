import hashlib
from django.db import models


class useInfo(models.Model):
    username = models.CharField(max_length=64, unique=True,verbose_name="用户名") #用户名
    password = models.CharField(max_length=64,verbose_name="密码") #密码
    name = models.CharField(max_length=64, unique=True,verbose_name="姓名") # 姓名
    phone = models.CharField(max_length=16,verbose_name="电话") #电话
    gender = models.CharField(max_length=16,verbose_name="性别") #性别
    email = models.EmailField(max_length=64,verbose_name="邮箱地址") #邮箱
    birthday = models.DateField(max_length=64,verbose_name="出生日期") # 出生日期
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间') #注册时间
    class Meta:
        verbose_name = '用户信息表'

