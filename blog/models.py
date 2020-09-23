import hashlib
from django.db import models

class UserInfo(models.Model):
    SEX_ITEMS=[
        (1,'男'),
        (2,'女'),
        (0,'未知')
    ]
    STATUS_ITEMS = [
        (1, '申请'),
        (2, '通过'),
        (0, '拒绝')
    ]
    name = models.CharField(max_length=128,verbose_name="用户名")
    password = models.CharField(max_length=64, verbose_name="密码")
    gender= models.IntegerField(choices=SEX_ITEMS,verbose_name="用户名")
    profession= models.CharField(max_length=128, verbose_name="职业")
    email = models.EmailField(verbose_name="Email")
    qq = models.CharField(max_length=128,verbose_name="QQ")
    phone = models.CharField(max_length=128,verbose_name="电话")
    status = models.IntegerField(choices=STATUS_ITEMS, default=0,verbose_name=
    "审核状态")
    create_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=
    '注册时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '用户信息表'

    # 类方法、将获取搜友信息的逻辑封装到models层中
    @classmethod
    def get_all(cls):
        return cls.objects.all()
